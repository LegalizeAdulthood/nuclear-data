#!/usr/bin/env python3
#
# ND812 disassembler
#
# Input formats supported:
#   16le    : one 12-bit word stored in a 16-bit little endian value
#   16be    : one 12-bit word stored in a 16-bit big endian value
#   pack3be : two 12-bit words packed into 3 bytes, big endian style
#   pack3le : two 12-bit words packed into 3 bytes, little endian style
#

import argparse


def oct12(v):
    return "%04o" % (v & 0o7777)


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--format", default="16be",
                        choices=["16le", "16be", "pack3le", "pack3be"])
    parser.add_argument("--origin", default="0")

    args = parser.parse_args()

    origin = parse_num(args.origin)

    with open(args.file, "rb") as f:
        data = f.read()

    words = load_words(data, args.format)

    disassemble(words, origin)


if __name__ == "__main__":
    main()
