# Instruction Set 

- Bit 0 is the most significant bit in the 12-bit word.
- Bit 11 is the least significant bit in the 12-bit word.

## Single Word Instructions

| Bits | Description |
|------|-------------|
| 0-3 | Opcode |
| 4 | Direct/Indirect |
| 5 | +/- Displacement Sign |
| 6-11 | Displacement |

## Literal Format

| Bits | Description |
|:----:|:------------|
| 0-3 | Operation |
| 4-5 | Instruction |
| 6-11 | Literal |

## Group 1 Format

| Bits | Description |
|:----:|:------------|
| 0-3 | `0010` |
| 4 | K |
| 5 | J |
| 6-7 | Shift/Rotate |
| 8-11 | Shift Count |

## Group 2 Format

| Bits | Description |
|:----:|:------------|
| 0-3 | `0011` |
| 4 | K |
| 5 | J |
| 6 | OV |
| 7 | Comp Set |
| 8 | Comp Clear |
| 9 | 0/1 |
| 10 | >= 0, < 0 |
| 11 | != 0 |

## Two Word Instructions

| Bits | Description |
|:----:|:------------|
| 0-2 | `000` |
| 3-6 | Instruction |
| 7 | Indirect |
| 8 | KJ Accumulator |
| 9 | Change Fields
| 10-11 | Field number |

# Instructions in Numerical Order

| Octal Value | Mnemonic | Description |
|------------:|:---------|:------------|
| 0000 | STOP | Halt the computer |
| 0101 | CHSF | High-speed forward to cassette EOT (TWIO) |
| 0102 | CSPF | space forward to cassette filemark (TWIO) |
| 0104 | CSFM | Write filemark on cassette (TWIO) |
| 0110 | CSET | Skip if cassette at EOT (TWIO) |
| 0121 | CHSR | High speed reverse to cassette BOT (TWIO) |
| 0122 | CSNE | Skip if no cassette errors (TWIO) |
| 0124 | CSTR | Skip if on-line cassette ready (TWIO) |
| 0130 | CSBT | Skip if cassette at BOT (TWIO) |
| 0141 | CCLF | Clear all cassette flags (TWIO) |
| 0142 | CSRR | Skip if cassette read flag = 1 (TWIO) |
| 0144 | CRDT | Transfer cassette buffer to J (TWIO) |
| 0151 | CWFM | Write filemark on cassette (TWIO) |
| 0152 | CSWR | Skip if cassette write flag = 1 (TWIO) |
| 0154 | CWRT | Transfer J to cassette buffer (TWIO) |
| 0240 | TWSMJ | Skip if J != memory |
| 0250 | TWSMK | Skip if K != memory |
| 0300 | TWDSZ | Decrement memory; skip if == 0 |
| 0340 | TWISZ | Increment memory; skip if == 0 |
| 0400 | TWSBJ | Subtract memory from J |
| 0410 | TWSBK | Subtract memory from K |
| 0440 | TWADJ | Add memory to J |
| 0450 | TWADK | Add memory to K |
| 0500 | TWLDJ | Load memory into J |
| 0510 | TWLDK | Load memory into K |
| 0540 | TWSTJ | Store J in memory |
| 0550 | TWSTK | Store K in memory |
| 0600 | TWJMP | Jump unconditionally |
| 0640 | TWJPS | Jump to subroutine |
| 0740 | TWIO | Two word I/O |
| 1000 | MPY | J*K to R, S |
| 1001 | DIV | J, K/R to J; remainder in K |
| 1002 | RFOV | Restore flag and overflow bits |
| 1003 | IOFF | Disable all interrupts |
| 1004 | IONH | Enable highest priority interrupt |
| 1005 | IONB | Enable class B and highest priority interrupts |
| 1006 | IONA | Enable class A and highest priority interrupts |
| 1007 | IONN | Enable all interrupts |
| 1010 | LJSW | Load J from Switch Register |
| 1011 | LJST | Load J from Status Bus |
| 1100 | AND J | Logical AND J,K to J |
| 1101 | LRFJ | Load R from J |
| 1102 | LJFR | Load J from R |
| 1103 | EXJR | Exchange J and R |
| 1120 | AJK J | J+K to J |
| 1121 | SJK J | J-K to J |
| 1122 | ADR J | R+J to J |
| 1123 | SBR J | R-J to J |
| 1124 | ADS J | S+J to J |
| 1125 | SBS J | S-J to J |
| 1130 | NAJK J | -(J+K) to J |
| 1131 | NSJK J | -(J-K) to J |
| 1132 | NADR J | -(R+J) to J |
| 1133 | NSBR J | -(R-J) to J |
| 1134 | NADS J | -(S+J) to J |
| 1135 | NSBS J | -(S-J) to J |
| 1140 | SFTZ J | Shift zeros left into J |
| 1160 | ROTD J | Rotate data left into J |
| 1200 | AND K | Logical AND J,K to K |
| 1201 | LSFK | Load S from K |
| 1202 | LKFS | Load K from S |
| 1203 | EXKS | Exchange K and S |
| 1204 | LKFJ | Load K from J |
| 1220 | AJK K | J+K to K |
| 1221 | SJK K | J-K to K |
| 1222 | ADR K | R+K to K |
| 1223 | SBR K | R-K to K |
| 1224 | ADS K | S+K to K |
| 1225 | SBS K | S-K to K |
| 1230 | NAJK K | -(J+K) to K |
| 1231 | NSJK K | -(J-K) to K |
| 1232 | NADR K | -(R+K) to K |
| 1233 | NSBR K | -(R-K) to K |
| 1234 | NADS K | -(S+K) to K |
| 1235 | NSBS K | -(S-K) to K |
| 1240 | SFTZ K | Shift zeroes left into K |
| 1260 | ROTD K | Rotate data left into K |
| 1300 | AND JK | Logical AND J,K to J,K |
| 1301 | LRSFJK | Load R from J; S from K |
| 1302 | LJKFRS | Load J from R; K from S |
| 1303 | EXJRKS | Exchange J and R; K and S |
| 1320 | AJK JK | J+K to J, K |
| 1321 | SJK JK | J-K to J, K |
| 1330 | NAJK JK | -(J+K) to J, K |
| 1331 | NSJK JK | -(J-K) to J, K |
| 1340 | SFTZ JK | Shift zeros left into J,K |
| 1360 | ROTD JK | Rotate data left into J,K |
| 1374 | EXJK | Exchange J and K |
| 1400 | IDLE | One cycle delay |
| 1401 | SNZ | Skip if flag bit != 0 |
| 1405 | SIZ | Skip if flag bit == 0 |
| 1410 | CLR | Clear flag bit |
| 1420 | CMP | Complement flag bit |
| 1430 | SET | Set flag bit = 1 |
| 1440 | SKPL | Skip on power low |
| 1441 | SNZ O | Skip if overflow bit != 0 |
| 1442 | SKIP | Skip unconditionally |
| 1445 | SIZ O | Skip if overflow bit == 0 |
| 1450 | CLR O | Clear overflow bit |
| 1460 | CMP O | Complement overflow bit |
| 1470 | SET O | Set overflow bit |
| 1500 | PION | Enable power interrupt |
| 1501 | SNZ J | Skip if J != 0 |
| 1502 | SIP J | Skip if J > 0 (positive) |
| 1504 | INC J | Increment J |
| 1505 | SIZ J | Skip if J == 0 |
| 1506 | SIN J | Skip if J < 0 |
| 1510 | CLR J | Clear J |
| 1520 | CMP J | Complement J |
| 1524 | NEG J | Negate J (two's complement) |
| 1530 | SET J | Set J = 7777 |
| 1600 | PIOF | Disable power interrupt |
| 1601 | SNZ K | Skip if K != 0 |
| 1602 | SIP K | Skip if K > 0 (positive) |
| 1604 | INC K | Increment K |
| 1605 | SIZ K | Skip if K == 0 |
| 1606 | SIN K | Skip if K < 0 |
| 1610 | CLR K | Clear K |
| 1620 | CMP K | Complement K |
| 1624 | NEG K | Negate K (two's complement) |
| 1630 | SET K | Set K = 7777 |
| 1701 | SNZ JK | Skip if J != 0 and K != 0 |
| 1702 | SIP JK | Skip if J > 0 and K > 0 |
| 1704 | INC JK | Increment J and K |
| 1705 | SIZ JK | Skip if J == 0 and K == 0 |
| 1706 | SIN JK | Skip if J < 0 and K < 0 |
| 1710 | CLR JK | Clear J and K |
| 1720 | CMP JK | Complement J and K |
| 1724 | NEG JK | Negate J and K (two's complement) |
| 1730 | SET JK | Set J = 7777 and K = 7777 |
| 20xx | ANDF | Logical AND J with memory |
| 21xx | ANDL | Logical AND J with immediate |
| 22xx | ADDL | Add immediate to J |
| 23xx | SUBL | Subtrace immediate from J |
| 2400 | SMJ | Skip if J != memory |
| 3000 | DSZ | Decrement memory; skip if == 0 |
| 3400 | ISZ | Increment memory; skip if == 0 |
| 4000 | SBJ | Subtract memory from J |
| 4400 | ADJ | Add memory to J |
| 5000 | LDJ | Load memory into J |
| 5400 | STJ | Store J in memory |
| 6000 | JMP | Jump unconditionally |
| 6400 | JPS | Jump to subroutine |
| 7000 | XCT | Execute instruction n |
| 7401 | TIF | Clear reader flag, read next character into reader buffer, set flag when done |
| 7402 | TIR | Clear reader flag and load J from reader buffer |
| 7403 | TRF | TIR and TIF combined |
| 7404 | TIS | Skip if reader flag = 1 |
| 7411 | TOC | Clear punch flag |
| 7412 | TOP | Clear punch flag, load punch buffer from J, punch data |
| 7413 | TCP | TOP and TOC combined |
| 7414 | TOS | Skip if punch flag = 1 |
| 7421 | HIF | Clear HS reader flag, read into HS reader buffer, set HS reader flag when done |
| 7422 | HIR | Clear HS reader flag, load J from HS reader buffer |
| 7423 | HRF | HIR and HIF combined |
| 7424 | HIS | Skip if HS reader flag = 1 |
| 7431 | HOP | Clear HS punch flag and punch HS buffer |
| 7432 | HOL | Clear HS punch flag and load HS punch buffer from J |
| 7433 | HLP | HOL and HOP combined |
| 7434 | HOS | Skip if HS punc flag = 1 |
| 7601 | CSLCT1 | Set cassette 1 on-line |
| 7602 | CSLCT2 | Set cassette 2 on-line |
| 7604 | CSLCT3 | Set cassette 3 on-line |
| 7720 | LDREG | Load JPS from J; INT from K |
| 7721 | LDJK | Load J from JPS; K from INT |
| 7722 | RJIB | Restore JPS and INT field bits |
