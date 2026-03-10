#!/usr/bin/env python3

import argparse


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
    0o1400: "IDLE",
    0o1410: "CLR",
    0o1420: "CMP",
    0o1430: "SET",
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


def decode(word, pc):
    if word in EXACT:
        return EXACT[word]

    lit = decode_literal(word)
    if lit:
        return lit

    rel = decode_relative(word, pc)
    if rel:
        return rel

    return ".WORD %04o" % word


def parse_tape(data):
    frames = []
    field = 0

    for b in data:

        if b == 0x80:
            continue

        if 0x84 <= b <= 0x87:
            field = b & 0x03
            frames.append(("FIELD", field))
            continue

        if b <= 0x3F:
            frames.append(("DATA", b))
            continue

    words = []
    i = 0

    while i < len(frames):

        t, v = frames[i]

        if t == "FIELD":
            words.append(("FIELD", v))
            i += 1
            continue

        if t == "DATA":

            if i + 1 >= len(frames):
                break

            t2, v2 = frames[i + 1]

            if t2 != "DATA":
                i += 1
                continue

            word = ((v & 0x3F) << 6) | (v2 & 0x3F)

            words.append(("WORD", word))
            i += 2
            continue

        i += 1

    return words


def disassemble(words):

    field = 0
    addr = 0

    for t, v in words:

        if t == "FIELD":
            field = v
            addr = 0
            print("")
            print("; field change -> %o" % field)
            continue

        if t == "WORD":

            phys = (field << 12) | addr

            text = decode(v, addr)

            print("%05o: %04o  %s" % (phys, v, text))

            addr += 1


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    with open(args.file, "rb") as f:
        data = f.read()

    words = parse_tape(data)

    disassemble(words)


if __name__ == "__main__":
    main()
