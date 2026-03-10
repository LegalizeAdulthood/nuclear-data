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
# ND812 paper tape assumptions used here:
#   0x00..0x3f  data frames
#   0x40..0x7f  record-start character with load address high 6 bits
#   0x80        leader/trailer fill
#   0x84..0x87  field change character, low 2 bits are the field number
#
# Record handling:
#   - leading zero bytes are ignored
#   - 0x80 leader/trailer bytes are ignored
#   - a record starts at a byte in 0x40..0x7f
#   - the next byte is the low 6 bits of the load address
#   - subsequent 0x00..0x3f bytes are payload frames until the next control
#   - the last complete 12-bit payload word is treated as the checksum word
#   - checksum test is done over:
#         load_address + all payload words
#     modulo 4096
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


def decode(words, i, origin):
    pc = (origin + i) & 0o7777
    w = words[i]

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


def pair_frames_to_words(frames):
    words = []
    i = 0

    while i + 1 < len(frames):
        w = ((frames[i] & 0x3F) << 6) | (frames[i + 1] & 0x3F)
        words.append(w)
        i += 2

    trailing = None
    if i < len(frames):
        trailing = frames[i] & 0x3F

    return words, trailing


def parse_ndpt_records(data):
    records = []

    pos = 0

    while pos < len(data) and data[pos] == 0x00:
        pos += 1

    while pos < len(data) and data[pos] == 0x80:
        pos += 1

    current_field = 0

    while pos < len(data):
        b = data[pos]

        if b == 0x00:
            pos += 1
            continue

        if b == 0x80:
            pos += 1
            continue

        if 0x84 <= b <= 0x87:
            current_field = b & 0x03
            pos += 1
            continue

        if 0x40 <= b <= 0x7F:
            rec_pos = pos
            load_hi = b & 0x3F
            pos += 1

            while pos < len(data) and data[pos] == 0x80:
                pos += 1

            if pos >= len(data):
                records.append({
                    "file_offset": rec_pos,
                    "field": current_field,
                    "load_addr": None,
                    "payload_words": [],
                    "checksum_word": None,
                    "checksum_sum": None,
                    "checksum_ok": False,
                    "trailing_frame": None,
                    "error": "record start at end of file",
                })
                break

            load_lo = data[pos] & 0x3F
            load_addr = (load_hi << 6) | load_lo
            pos += 1

            frames = []
            while pos < len(data):
                b2 = data[pos]

                if b2 == 0x80:
                    pos += 1
                    continue

                if b2 == 0x00:
                    frames.append(0)
                    pos += 1
                    continue

                if b2 < 0x40:
                    frames.append(b2 & 0x3F)
                    pos += 1
                    continue

                break

            words, trailing_frame = pair_frames_to_words(frames)

            checksum_word = None
            payload_words = []

            if words:
                payload_words = words[:-1]
                checksum_word = words[-1]

            checksum_sum = None
            checksum_ok = False

            if trailing_frame is None:
                checksum_sum = load_addr
                for w in words:
                    checksum_sum = (checksum_sum + w) & 0x0FFF
                checksum_ok = (checksum_sum == 0)

            records.append({
                "file_offset": rec_pos,
                "field": current_field,
                "load_addr": load_addr,
                "payload_words": payload_words,
                "checksum_word": checksum_word,
                "checksum_sum": checksum_sum,
                "checksum_ok": checksum_ok,
                "trailing_frame": trailing_frame,
                "error": None,
            })
            continue

        pos += 1

    return records


def disassemble_ndpt_records(records):
    recno = 0

    for rec in records:
        recno += 1

        print(";")
        print("; record %d" % recno)
        print("; file offset: 0x%X" % rec["file_offset"])
        print("; field: %o" % rec["field"])

        if rec["load_addr"] is None:
            print("; load address: <missing>")
            print("; error: %s" % rec["error"])
            continue

        full_load = (rec["field"] << 12) | rec["load_addr"]
        print("; load address: %04o (physical %05o)" %
              (rec["load_addr"], full_load))

        if rec["checksum_word"] is None:
            print("; checksum word: <missing>")
        else:
            print("; checksum word: %04o" % rec["checksum_word"])

        if rec["trailing_frame"] is not None:
            print("; checksum: incomplete record, trailing unpaired frame %02o" %
                  rec["trailing_frame"])
            print("; checksum match: NO")
        elif rec["checksum_sum"] is None:
            print("; checksum: <not computed>")
            print("; checksum match: NO")
        else:
            print("; checksum sum: %04o" % rec["checksum_sum"])
            if rec["checksum_ok"]:
                print("; checksum match: YES")
            else:
                print("; checksum match: NO")

        if not rec["payload_words"]:
            print("; no payload words")
            continue

        disassemble(rec["payload_words"], rec["load_addr"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--format", default="16be",
                        choices=["16le", "16be", "pack3le", "pack3be", "ndpt"])
    parser.add_argument("--origin", default="0")

    args = parser.parse_args()

    with open(args.file, "rb") as f:
        data = f.read()

    if args.format == "ndpt":
        records = parse_ndpt_records(data)
        disassemble_ndpt_records(records)
        return

    origin = parse_num(args.origin)
    words = load_words(data, args.format)
    disassemble(words, origin)


if __name__ == "__main__":
    main()
