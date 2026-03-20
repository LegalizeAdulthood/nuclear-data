#!/usr/bin/env python3
#
# ND812 disassembler
#
# Input format:
#   ND812 binary paper tape dump
#
# ND812 binary paper tape format used here:
#
#   Leader/trailer:
#       0x80 bytes repeated. These are ignored.
#
#   Field change:
#       0x84..0x87
#       low two bits select memory field.
#       Field change characters are not included in the checksum.
#
#   Record structure:
#
#       leader/trailer
#       field change
#       origin address
#       payload
#       checksum word
#       leader/trailer
#
#   Origin address:
#       two bytes
#       first byte has 0x40 set
#       low 6 bits of first byte are the high 6 bits of the 12-bit origin
#       second byte supplies the low 6 bits
#
#   Payload:
#       ordinary 6-bit data frames, 0x00..0x3F
#       pairs of frames form 12-bit words
#
#           word = (frame1 << 6) | frame2
#
#   Checksum word:
#       two bytes
#       first byte has 0x40 set
#       low 6 bits of first byte are the high 6 bits of the 12-bit checksum
#       second byte supplies the low 6 bits
#
#   Checksum comparison:
#       Compute the checksum from:
#
#           origin + payload words
#
#       modulo 4096.
#
#       Exclude:
#           field change characters
#           tape checksum word itself
#
#       The checksum word stored on tape is expected to be:
#
#           (-computed_checksum) & 0xFFF
#
#       Equivalently:
#
#           (computed_checksum + tape_checksum_word) & 0xFFF == 0
#

import argparse
import os


def oct12(v):
    return "%04o" % (v & 0o7777)


def oct15(v):
    return "%05o" % (v & 0o77777)


EXACT = {
    0o0000: "STOP",
    0o1000: "MPY",
    0o1001: "DIV",
    0o1002: "RFOV",
    0o1003: "IOFF",
    0o1004: "IONH",
    0o1005: "IONB",
    0o1006: "IONA",
    0o1007: "IONN",
    0o1010: "LJSW",
    0o1011: "LJST",
    0o1101: "LRFJ",
    0o1102: "LJFR",
    0o1103: "EXJR",
    0o1201: "LSFK",
    0o1202: "LKFS",
    0o1203: "EXKS",
    0o1204: "LKFJ",
    0o1301: "LRSFJK",
    0o1302: "LJKFRS",
    0o1303: "EXJRKS",
    0o1374: "EXJK",
    0o1400: "IDLE",
    0o1410: "CLR",
    0o1420: "CMP",
    0o1430: "SET",
    0o1500: "PION",
    0o1600: "PIOF",
    0o7401: "TIF",
    0o7402: "TIR",
    0o7403: "TRF",
    0o7404: "TIS",
    0o7411: "TOC",
    0o7412: "TOP",
    0o7413: "TCP",
    0o7414: "TOS",
    0o7720: "LDREG",  # Load JPS from J, INT from K
    0o7721: "LDJK",   # Load J from JPS, K from INT
    0o7722: "RJIB",   # Set JPS and INT status
}


def decode_literal(word):
    op = word & 0o7700
    lit = word & 0o0077

    if op == 0o2100:
        return "ANDL", "%02o" % lit
    if op == 0o2200:
        return "ADDL", "%02o" % lit
    if op == 0o2300:
        return "SUBL", "%02o" % lit

    return None, None


def decode_relative(word, pc):
    op = (word >> 8) & 0xF

    table = {
        4: "ANDF",   # 0o20xx
        5: "SMJ",    # 0o24xx
        6: "DSZ",    # 0o30xx
        7: "ISZ",    # 0o34xx
        8: "SBJ",    # 0o40xx
        9: "ADJ",    # 0o44xx
        10: "LDJ",   # 0o50xx
        11: "STJ",   # 0o54xx
        12: "JMP",   # 0o60xx
        13: "JPS",   # 0o64xx
        14: "XCT",   # 0o70xx
    }

    if op not in table:
        return None, None, None

    mnem = table[op]
    indirect = (word & 0o0200) != 0
    neg = (word & 0o0100) != 0
    disp = word & 0o0077

    sign_char = '-' if neg else '+'
    signed_disp = -disp if neg else disp

    target = (pc + signed_disp) & 0o7777
    if indirect:
        mnem += "@"
    operand = ".%s%o" % (sign_char, disp)
    comment = ".%s%o = %04o" % (sign_char, disp, target)

    return mnem, operand, comment


def decode_group1(word):
    k = (word & 0o0200) != 0
    j = (word & 0o0100) != 0

    if not (k or j):
        return None, None

    reg = ""
    if j:
        reg += "J"
    if k:
        reg += "K"

    # Non-shift instructions
    negate = (word & 0o0010) != 0
    base = word & 0o7467  # mask out J/K select and negate bits

    # (mnemonic, has_jk_form)
    group1_ops = {
        0o1000: ("AND", True),
        0o1020: ("AJK", True),
        0o1021: ("SJK", True),
        0o1022: ("ADR", False),
        0o1023: ("SBR", False),
        0o1024: ("ADS", False),
        0o1025: ("SBS", False),
    }

    if base in group1_ops:
        mnem, has_jk = group1_ops[base]
        if j and k and not has_jk:
            return None, None
        if negate:
            mnem = "N" + mnem
        return mnem, reg

    # Shift instructions: shift count in bits 8-11 (low 4 bits)
    shift_base = word & 0o7460  # mask out J/K and shift count
    shift_count = word & 0o0017

    # (mnemonic, has_jk_form)
    group1_shift_ops = {
        0o1040: ("SFTZ", True),
        0o1060: ("ROTD", True),
    }

    if shift_base in group1_shift_ops:
        mnem, has_jk = group1_shift_ops[shift_base]
        if j and k and not has_jk:
            return None, None
        return mnem, "%s,%o" % (reg, shift_count)

    return None, None


def decode_group2(word):
    """Decode Group 2 instructions (skip instructions and clear/complement/set).

    Bit numbering: bit 0 is MSB, bit 11 is LSB
    Bit 4 = K accumulator (0o0200)
    Bit 5 = J accumulator (0o0100)
    Bit 6 = Overflow (0o0040)
    Bits 7-8 encode operation:
        00: Skip instruction
        01: CLR (bit 8 set)
        10: CMP (bit 7 set)
        11: SET (both bits 7 and 8 set)

    If no register bits are set, the flag bit is implied (no operand output).
    """
    k = (word & 0o0200) != 0
    j = (word & 0o0100) != 0
    o = (word & 0o0040) != 0

    # Build register operand string (empty string if flag bit)
    reg = ""
    if j:
        reg += "J"
    if k:
        reg += "K"
    if o:
        reg += "O"

    # If no register bits are set, it's a flag bit operation
    # Only handle skip instructions here (CLR/CMP/SET are in EXACT table)
    if not (k or j or o):
        # Check operation type in bits 7-8
        bit7 = (word & 0o0020) != 0
        bit8 = (word & 0o0010) != 0

        if not bit7 and not bit8:
            # Skip instruction on flag bit: condition in bits 9-11
            condition = word & 0o0007
            skip_ops = {
                0o01: "SNZ",  # Skip if Non-Zero
                0o05: "SIZ",  # Skip if Zero
            }
            if condition in skip_ops:
                return skip_ops[condition], ""

        return None, None

    # Check operation type in bits 7-8
    bit7 = (word & 0o0020) != 0
    bit8 = (word & 0o0010) != 0

    if not bit7 and not bit8:
        # Skip instruction or INC: condition in bits 9-11
        condition = word & 0o0007
        if condition == 0o04:
            return "INC", reg
        skip_ops = {
            0o00: "SKPL",  # Skip on Power Low
            0o01: "SNZ",  # Skip if Non-Zero
            0o02: "SIP",  # Skip if Positive
            0o05: "SIZ",  # Skip if Zero
            0o06: "SIN",  # Skip if Negative
        }
        if condition in skip_ops:
            return skip_ops[condition], reg
    elif not bit7 and bit8:
        return "CLR", reg
    elif bit7 and not bit8:
        # NEG or CMP
        condition = word & 0o0007
        if condition == 0o04:
            return "NEG", reg
        return "CMP", reg
    elif bit7 and bit8:
        return "SET", reg

    return None, None


def decode_single_word(word):
    pass


def decode_two_word(words, i, origin):
    pass


def decode_instruction(word, pc):
    """Decode a single instruction word and return (mnemonic, operand, comment)."""
    # Check EXACT matches first (highest priority)
    if word in EXACT:
        return EXACT[word], "", ""

    if (0o7400 & word) == 0o1400:
        mnem, operand = decode_group2(word)
        if mnem:
            return mnem, operand, ""
    elif (0o7400 & word) == 0o1000:
        mnem, operand = decode_group1(word)
        if mnem:
            return mnem, operand, ""
    elif (0o7000 & word) == 0:
        decode_two_word(None, 0, 0)
    else:
        decode_single_word(word)

    mnem, operand = decode_literal(word)
    if mnem:
        return mnem, operand, ""

    mnem, operand, comment = decode_relative(word, pc)
    if mnem:
        return mnem, operand, comment

    return "%04o" % word, "", ""


def format_line(label="", mnemonic="", operand="", comment=""):
    """Format a line in ND812 assembler syntax.

    Columns 1-8:   label (followed by comma if present)
    Columns 9-16:  mnemonic
    Columns 17+:   operand
    Column 41+:    comment (prefixed with /)
    """
    if label:
        label = label + ","

    label_field = label.ljust(8)
    mnem_field = mnemonic.ljust(8)

    if comment:
        if operand:
            line = f"{label_field}{mnem_field}{operand}"
            line = line.ljust(40) + "/" + comment
        else:
            line = f"{label_field}{mnem_field}"
            if line.rstrip():
                line = line.ljust(40) + "/" + comment
            else:
                line = "/" + comment
    else:
        line = f"{label_field}{mnem_field}{operand}"

    return line.rstrip()


def format_comment(text):
    """Format a full-line comment."""
    return "/" + text


def form_word(a, b):
    """Form a 12-bit word from two 6-bit frames."""
    return ((a & 0x3F) << 6) | (b & 0x3F)


def process_tape_stream(data, filename):
    """Process and disassemble ND812 paper tape data as it is encountered."""
    pos = 0
    field = None
    record_num = 0

    # Output filename
    print(format_comment(" " + filename))

    # Count and skip initial null bytes (only initial consecutive NULs)
    null_start = pos
    while pos < len(data) and data[pos] == 0x00:
        pos += 1
    null_count = pos - null_start

    if null_count > 0:
        print(format_comment(" %04o (%d) NUL bytes" % (null_count, null_count)))

    # Count leader/trailer bytes (everything from here until first non-0x80, non-0x00 byte)
    # This includes 0x80 bytes and any interspersed 0x00 bytes
    leader_start = pos
    while pos < len(data) and (data[pos] == 0x80 or data[pos] == 0x00):
        pos += 1
    leader_count = pos - leader_start

    if leader_count > 0:
        print(format_comment(" %04o (%d) leader bytes" % (leader_count, leader_count)))

    # If no more data, we're done
    if pos >= len(data):
        return

    while pos < len(data):
        b = data[pos]

        # Field change directive (100001xx)
        if 0x84 <= b <= 0x87:
            field = b & 0x03
            print(format_line(mnemonic="[FIELD", operand="%d" % field))
            pos += 1
            continue

        # Start of new record
        record_num += 1
        rec_start = pos

        print(format_comment(""))
        print(format_comment(" record %d" % record_num))
        print(format_comment(" file offset: 0x%X" % rec_start))

        # Read origin address
        if pos + 1 >= len(data):
            print(format_comment(" ERROR: truncated origin"))
            break

        if not (data[pos] & 0x40):
            print(format_comment(" ERROR: Expected marked byte at position %d, got 0x%02x" % (pos, data[pos])))
            break

        origin = form_word(data[pos], data[pos + 1])
        pos += 2
        pc = origin

        # Output origin directive
        print(format_line(mnemonic="*%04o" % origin))

        # Process payload words and disassemble immediately
        checksum = origin
        tape_checksum = None

        while pos < len(data):
            b = data[pos]

            # Marked byte indicates checksum word
            if (b & 0x40):
                tape_checksum = form_word(data[pos], data[pos + 1])
                pos += 2
                break

            # FIELD directive in payload (unusual but handle it)
            if 0x84 <= b <= 0x87:
                pos += 1
                continue

            # Read payload word
            if pos + 1 >= len(data):
                print(format_comment(" ERROR: truncated payload word"))
                pos += 1
                break

            b2 = data[pos + 1]

            if (b2 & 0x80):
                print(format_comment(" ERROR: Corrupted payload second byte: 0x%02x at position %d" % (b2, pos)))
                pos += 2
                continue

            word = form_word(b, b2)
            checksum = (checksum + word) & 0xFFF
            pos += 2

            # Disassemble and output immediately
            mnem, operand, comment = decode_instruction(word, pc)
            if comment:
                full_comment = " " + comment
            else:
                raw_comment = "%04o" % word
                full_comment = " " + raw_comment
            print(format_line(mnemonic=mnem, operand=operand, comment=full_comment))

            pc = (pc + 1) & 0o7777

        # Output checksum information
        if tape_checksum is None:
            print(format_comment(" ERROR: Missing checksum word"))
        else:
            if (checksum + tape_checksum) & 0xFFF != 0:
                print(format_comment(" checksum: %04o (MISMATCH: computed %04o)" % (tape_checksum, checksum)))
            else:
                print(format_comment(" checksum: %04o" % tape_checksum))

        # Skip trailing leader/trailer
        while pos < len(data) and data[pos] == 0x80:
            pos += 1


def main():
    parser = argparse.ArgumentParser(description="ND812 disassembler for binary paper tape dumps")
    parser.add_argument("file", help="ND812 binary paper tape dump file")

    args = parser.parse_args()

    with open(args.file, "rb") as f:
        data = f.read()

    # Use just the basename for output
    filename = os.path.basename(args.file)
    process_tape_stream(data, filename)


if __name__ == "__main__":
    main()
