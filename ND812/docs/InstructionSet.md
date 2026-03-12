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

| Value | Mnemonic | Format | Description |
|------------:|:---------|:-------|:------------|
| 0000 | STOP   | Single | Halt the computer |
| 0101 | CHSF   | Double | High-speed forward to cassette EOT (TWIO) |
| 0102 | CSPF   | Double | Space forward to cassette filemark (TWIO) |
| 0104 | CSFM   | Double | Write filemark on cassette (TWIO) |
| 0110 | CSET   | Double | Skip if cassette at EOT (TWIO) |
| 0121 | CHSR   | Double | High speed reverse to cassette BOT (TWIO) |
| 0122 | CSNE   | Double | Skip if no cassette errors (TWIO) |
| 0124 | CSTR   | Double | Skip if on-line cassette ready (TWIO) |
| 0130 | CSBT   | Double | Skip if cassette at BOT (TWIO) |
| 0141 | CCLF   | Double | Clear all cassette flags (TWIO) |
| 0142 | CSRR   | Double | Skip if cassette read flag = 1 (TWIO) |
| 0144 | CRDT   | Double | Transfer cassette buffer to J (TWIO) |
| 0151 | CWFM   | Double | Write filemark on cassette (TWIO) |
| 0152 | CSWR   | Double | Skip if cassette write flag = 1 (TWIO) |
| 0154 | CWRT   | Double | Transfer J to cassette buffer (TWIO) |
| 0240 | TWSMJ  | Double | Skip if J != memory |
| 0250 | TWSMK  | Double | Skip if K != memory |
| 0300 | TWDSZ  | Double | Decrement memory; skip if == 0 |
| 0340 | TWISZ  | Double | Increment memory; skip if == 0 |
| 0400 | TWSBJ  | Double | Subtract memory from J |
| 0410 | TWSBK  | Double | Subtract memory from K |
| 0440 | TWADJ  | Double | Add memory to J |
| 0450 | TWADK  | Double | Add memory to K |
| 0500 | TWLDJ  | Double | Load memory into J |
| 0510 | TWLDK  | Double | Load memory into K |
| 0540 | TWSTJ  | Double | Store J in memory |
| 0550 | TWSTK  | Double | Store K in memory |
| 0600 | TWJMP  | Double | Jump unconditionally |
| 0640 | TWJPS  | Double | Jump to subroutine |
| 0740 | TWIO   | Double | Two word I/O |
| 1000 | MPY    | Single | J*K to R, S |
| 1001 | DIV    | Single | J, K/R to J; remainder in K |
| 1002 | RFOV   | Single | Restore flag and overflow bits |
| 1003 | IOFF   | Single | Disable all interrupts |
| 1004 | IONH   | Single | Enable highest priority interrupt |
| 1005 | IONB   | Single | Enable class B and highest priority interrupts |
| 1006 | IONA   | Single | Enable class A and highest priority interrupts |
| 1007 | IONN   | Single | Enable all interrupts |
| 1010 | LJSW   | Single | Load J from Switch Register |
| 1011 | LJST   | Single | Load J from Status Bus |
| 1100 | AND J  | Single | Logical AND J,K to J |
| 1200 | AND K  | Single | Logical AND J,K to K |
| 1300 | AND JK | Single | Logical AND J,K to J,K |
| 1101 | LRFJ   | Single | Load R from J |
| 1102 | LJFR   | Single | Load J from R |
| 1201 | LSFK   | Single | Load S from K |
| 1202 | LKFS   | Single | Load K from S |
| 1103 | EXJR   | Single | Exchange J and R |
| 1120 | AJK J  | Single | J+K to J |
| 1121 | SJK J  | Single | J-K to J |
| 1122 | ADR J  | Single | R+J to J |
| 1123 | SBR J  | Single | R-J to J |
| 1124 | ADS J  | Single | S+J to J |
| 1125 | SBS J  | Single | S-J to J |
| 1130 | NAJK J | Single | -(J+K) to J |
| 1131 | NSJK J | Single | -(J-K) to J |
| 1132 | NADR J | Single | -(R+J) to J |
| 1133 | NSBR J | Single | -(R-J) to J |
| 1134 | NADS J | Single | -(S+J) to J |
| 1135 | NSBS J | Single | -(S-J) to J |
| 1140 | SFTZ J | Single | Shift zeros left into J |
| 1160 | ROTD J | Single | Rotate data left into J |
| 1203 | EXKS   | Single | Exchange K and S |
| 1204 | LKFJ   | Single | Load K from J |
| 1220 | AJK K  | Single | J+K to K |
| 1221 | SJK K  | Single | J-K to K |
| 1222 | ADR K  | Single | R+K to K |
| 1223 | SBR K  | Single | R-K to K |
| 1224 | ADS K  | Single | S+K to K |
| 1225 | SBS K  | Single | S-K to K |
| 1230 | NAJK K | Single | -(J+K) to K |
| 1231 | NSJK K | Single | -(J-K) to K |
| 1232 | NADR K | Single | -(R+K) to K |
| 1233 | NSBR K | Single | -(R-K) to K |
| 1234 | NADS K | Single | -(S+K) to K |
| 1235 | NSBS K | Single | -(S-K) to K |
| 1240 | SFTZ K | Single | Shift zeroes left into K |
| 1260 | ROTD K | Single | Rotate data left into K |
| 1301 | LRSFJK | Single | Load R from J; S from K |
| 1302 | LJKFRS | Single | Load J from R; K from S |
| 1303 | EXJRKS | Single | Exchange J and R; K and S |
| 1320 | AJK JK | Single | J+K to J, K |
| 1321 | SJK JK | Single | J-K to J, K |
| 1330 | NAJK JK | Single | -(J+K) to J, K |
| 1331 | NSJK JK | Single | -(J-K) to J, K |
| 1340 | SFTZ JK | Single | Shift zeros left into J,K |
| 1360 | ROTD JK | Single | Rotate data left into J,K |
| 1374 | EXJK   | Single | Exchange J and K |
| 1400 | IDLE   | Single | One cycle delay |
| 1401 | SNZ    | Single | Skip if flag bit != 0 |
| 1405 | SIZ    | Single | Skip if flag bit == 0 |
| 1410 | CLR    | Single | Clear flag bit |
| 1420 | CMP    | Single | Complement flag bit |
| 1430 | SET    | Single | Set flag bit = 1 |
| 1440 | SKPL   | Single | Skip on power low |
| 1441 | SNZ O  | Single | Skip if overflow bit != 0 |
| 1442 | SKIP   | Single | Skip unconditionally |
| 1445 | SIZ O  | Single | Skip if overflow bit == 0 |
| 1450 | CLR O  | Single | Clear overflow bit |
| 1460 | CMP O  | Single | Complement overflow bit |
| 1470 | SET O  | Single | Set overflow bit |
| 1500 | PION   | Single | Enable power interrupt |
| 1600 | PIOF   | Single | Disable power interrupt |
| 1501 | SNZ J  | Single | Skip if J != 0 |
| 1502 | SIP J  | Single | Skip if J > 0 (positive) |
| 1504 | INC J  | Single | Increment J |
| 1505 | SIZ J  | Single | Skip if J == 0 |
| 1506 | SIN J  | Single | Skip if J < 0 |
| 1510 | CLR J  | Single | Clear J |
| 1520 | CMP J  | Single | Complement J |
| 1524 | NEG J  | Single | Negate J (two's complement) |
| 1530 | SET J  | Single | Set J = 7777 |
| 1601 | SNZ K  | Single | Skip if K != 0 |
| 1602 | SIP K  | Single | Skip if K > 0 (positive) |
| 1604 | INC K  | Single | Increment K |
| 1605 | SIZ K  | Single | Skip if K == 0 |
| 1606 | SIN K  | Single | Skip if K < 0 |
| 1610 | CLR K  | Single | Clear K |
| 1620 | CMP K  | Single | Complement K |
| 1624 | NEG K  | Single | Negate K (two's complement) |
| 1630 | SET K  | Single | Set K = 7777 |
| 1701 | SNZ JK | Single | Skip if J != 0 and K != 0 |
| 1702 | SIP JK | Single | Skip if J > 0 and K > 0 |
| 1704 | INC JK | Single | Increment J and K |
| 1705 | SIZ JK | Single | Skip if J == 0 and K == 0 |
| 1706 | SIN JK | Single | Skip if J < 0 and K < 0 |
| 1710 | CLR JK | Single | Clear J and K |
| 1720 | CMP JK | Single | Complement J and K |
| 1724 | NEG JK | Single | Negate J and K (two's complement) |
| 1730 | SET JK | Single | Set J = 7777 and K = 7777 |
| 20xx | ANDF   | Single | Logical AND J with memory |
| 21xx | ANDL   | Literal | Logical AND J with immediate |
| 22xx | ADDL   | Literal | Add immediate to J |
| 23xx | SUBL   | Literal | Subtract immediate from J |
| 2400 | SMJ    | Single | Skip if J != memory |
| 3000 | DSZ    | Single | Decrement memory; skip if == 0 |
| 3400 | ISZ    | Single | Increment memory; skip if == 0 |
| 4000 | SBJ    | Single | Subtract memory from J |
| 4400 | ADJ    | Single | Add memory to J |
| 5000 | LDJ    | Single | Load memory into J |
| 5400 | STJ    | Single | Store J in memory |
| 6000 | JMP    | Single | Jump unconditionally |
| 6400 | JPS    | Single | Jump to subroutine |
| 7000 | XCT    | Single | Execute instruction n |
| 7401 | TIF    | Single | Clear reader flag, read next character into reader buffer, set flag when done |
| 7402 | TIR    | Single | Clear reader flag and load J from reader buffer |
| 7403 | TRF    | Single | TIR and TIF combined |
| 7404 | TIS    | Single | Skip if reader flag = 1 |
| 7411 | TOC    | Single | Clear punch flag |
| 7412 | TOP    | Single | Clear punch flag, load punch buffer from J, punch data |
| 7413 | TCP    | Single | TOP and TOC combined |
| 7414 | TOS    | Single | Skip if punch flag = 1 |
| 7421 | HIF    | Single | Clear HS reader flag, read into HS reader buffer, set HS reader flag when done |
| 7422 | HIR    | Single | Clear HS reader flag, load J from HS reader buffer |
| 7423 | HRF    | Single | HIR and HIF combined |
| 7424 | HIS    | Single | Skip if HS reader flag = 1 |
| 7431 | HOP    | Single | Clear HS punch flag and punch HS buffer |
| 7432 | HOL    | Single | Clear HS punch flag and load HS punch buffer from J |
| 7433 | HLP    | Single | HOL and HOP combined |
| 7434 | HOS    | Single | Skip if HS punc flag = 1 |
| 7601 | CSLCT1 | Single | Set cassette 1 on-line |
| 7602 | CSLCT2 | Single | Set cassette 2 on-line |
| 7604 | CSLCT3 | Single | Set cassette 3 on-line |
| 7720 | LDREG  | Single | Load JPS from J; INT from K |
| 7721 | LDJK   | Single | Load J from JPS; K from INT |
| 7722 | RJIB   | Single | Restore JPS and INT field bits |
