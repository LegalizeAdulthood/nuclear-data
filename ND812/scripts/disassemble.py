#!/usr/bin/env python3
#
# ND812 disassembler
#
# Input formats supported:
#   16le    : one 12-bit word stored in a 16-bit little endian value
#   16be    : one 12-bit word stored in a 16-bit big endian value
#   pack3be : two 12-bit words packed into 3 bytes, big endian style
#   pack3le : two 12-bit words packed into 3 bytes, little endian style
#   ndpt    : ND812 binary paper tape dump
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


def oct12(v):
    return "%04o" % (v & 0o7777)


def oct15(v):
    return "%05o" % (v & 0o77777)


def load_words(data, fmt):
    words = []

    if fmt == "16le":
        if len(data) % 2:
            raise ValueError("input length must be even")
        for i in range(0, len(data), 2):
            w = data[i] | (data[i + 1] << 8)
            words.append(w & 0x0FFF)
        return words

    if fmt == "16be":
        if len(data) % 2:
            raise ValueError("input length must be even")
        for i in range(0, len(data), 2):
            w = (data[i] << 8) | data[i + 1]
            words.append(w & 0x0FFF)
        return words

    if fmt == "pack3be":
        if len(data) % 3:
            raise ValueError("length must be multiple of 3")
        for i in range(0, len(data), 3):
            b0 = data[i]
            b1 = data[i + 1]
            b2 = data[i + 2]
            w1 = ((b0 << 4) | (b1 >> 4)) & 0x0FFF
            w2 = (((b1 & 0x0F) << 8) | b2) & 0x0FFF
            words.append(w1)
            words.append(w2)
        return words

    if fmt == "pack3le":
        if len(data) % 3:
            raise ValueError("length must be multiple of 3")
        for i in range(0, len(data), 3):
            b0 = data[i]
            b1 = data[i + 1]
            b2 = data[i + 2]
            w1 = (b0 | ((b1 & 0x0F) << 8)) & 0x0FFF
            w2 = ((b2 << 4) | (b1 >> 4)) & 0x0FFF
            words.append(w1)
            words.append(w2)
        return words

    raise ValueError("unsupported format")


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
    0o1101: "LRF",
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
}


def decode_literal(word):
    op = word & 0o7700
    lit = word & 0o0077

    if op == 0o2100:
        return "ANDL %02o" % lit
    if op == 0o2200:
        return "ADDL %02o" % lit
    if op == 0o2300:
        return "SUBL %02o" % lit

    return None


def decode_relative(word, pc):
    op = (word >> 8) & 0xF

    table = {
        0o2: "ANDF",
        0o3: "DSZ",
        0o4: "SBJ",
        0o5: "LDJ",
        0o6: "JMP",
        0o7: "XCT",
    }

    if op not in table:
        return None

    mnem = table[op]
    indirect = (word & 0o0200) != 0
    neg = (word & 0o0100) != 0
    disp = word & 0o0077

    if neg:
        disp = -disp

    target = (pc + disp) & 0o7777
    mode = "@ " if indirect else ""

    return "%-6s %s%+o ; %04o" % (mnem, mode, disp, target)


def decode_group1(word):
    pass


def decode_group2(word):
    pass


def decode_single_word(word):
    pass


def decode_two_word(words, i, origin):
    pass


def decode(words, i, origin):
    pc = (origin + i) & 0o7777
    w = words[i]

    if (0o7400 & w) == 0o1400:
        decode_group2(w)
    elif (0o7400 & w) == 0o1000:
        decode_group1(w)
    elif (0o7000 & w) == 0:
        decode_two_word(words, i)
    else:
        decode_single_word(w)

    if w in EXACT:
        return 1, EXACT[w]

    lit = decode_literal(w)
    if lit:
        return 1, lit

    rel = decode_relative(w, pc)
    if rel:
        return 1, rel

    return 1, ".WORD %04o" % w


def disassemble(words, origin):
    i = 0

    while i < len(words):
        pc = (origin + i) & 0o7777
        size, text = decode(words, i, origin)
        raw = " ".join(oct12(words[i + j]) for j in range(size))
        print("%04o: %-9s %s" % (pc, raw, text))
        i += size


def parse_num(text):
    text = text.strip()

    if text.startswith("0o"):
        return int(text, 8)

    if all(c in "01234567" for c in text):
        return int(text, 8)

    return int(text)


def form_word(a, b):
    return ((a & 0x3F) << 6) | (b & 0x3F)


# The origin and check sum words consist of two frames:
#   01xx xxxx
#   00xx xxxx
# The first frame has bit 7 set and is the high 6 bits of the word.
# The second frame has bit 7 clear and is the low 6 bits of the word.
#
def get_marked_word(data, pos):
    if pos >= len(data) - 1:
        raise RuntimeError("Insufficient data")

    if not (data[pos] & 0x40):
        raise ValueError(f"Expected marked byte at {pos}, got {data[pos]} instead.")

    return form_word(data[pos], data[pos + 1])


def parse_ndpt_records(data):
    records = []
    pos = 0
    field = None

    while pos < len(data) and data[pos] == 0x00:
        pos += 1

    while pos < len(data) and data[pos] == 0x80:
        pos += 1

    while pos < len(data):
        b = data[pos]

        # 100001xx is from the FIELD assembler directive
        if 0x84 <= b <= 0x87:
            field = b & 0x03
            pos += 1
            continue

        rec_start = pos

        if pos + 1 >= len(data):
            records.append({
                "field": field,
                "origin": None,
                "payload": [],
                "tape_checksum": None,
                "computed_checksum": None,
                "expected_checksum": None,
                "checksum_ok": False,
                "file_offset": rec_start,
                "error": "truncated origin",
            })
            break

        origin = get_marked_word(data, pos)
        pos += 2

        payload = []
        checksum = origin
        tape_checksum = None
        error = None

        while pos < len(data):
            b = data[pos]

            # First frame with bit 7 set indicates
            # end of payload and start of checksum word
            if (b & 0x40):
                tape_checksum = get_marked_word(data, pos)
                pos += 2
                break

            # FIELD directive frames are 100001xx
            if (b & 0x84):
                w = b << 6
                payload.append(w)
                pos += 1
                continue

            if pos + 1 >= len(data):
                error = "truncated payload word"
                pos += 1
                break

            b2 = data[pos + 1]

            if (b2 & 0x80):
                raise ValueError(f"Corrupted payload second byte: 0x{b2:x} at position {pos}")

            w = form_word(b, b2)
            checksum += w
            checksum %= 0xFFF
            payload.append(w)
            pos += 2

        if tape_checksum is None:
            raise ValueError(f"Missing checksum word at position {pos}")

        if checksum != tape_checksum:
            print(f"Checksum mismatch: expected {tape_checksum:o}, got {checksum:o}")

        records.append({
            "field": field,
            "origin": origin,
            "payload": payload,
            "tape_checksum": tape_checksum,
            "file_offset": rec_start
        })

    return records


def disassemble_records(records):
    for i, r in enumerate(records, 1):
        print("/")
        print("/ record %d" % i)
        print("/ file offset: 0x%X" % r["file_offset"])

        if not r["field"] is None:
            print("        FIELD   %d" % r["field"])
        print("        *%04o" % r["origin"])

        print("/ checksum: %04o" % r["tape_checksum"])

        if r["payload"]:
            disassemble(r["payload"], r["origin"])
        else:
            print("/ no payload words")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--format", default="ndpt",
                        choices=["16le", "16be", "pack3le", "pack3be", "ndpt"])
    parser.add_argument("--origin", default="0")

    args = parser.parse_args()

    with open(args.file, "rb") as f:
        data = f.read()

    if args.format == "ndpt":
        records = parse_ndpt_records(data)
        disassemble_records(records)
        return

    words = load_words(data, args.format)
    origin = parse_num(args.origin)
    disassemble(words, origin)


if __name__ == "__main__":
    main()
