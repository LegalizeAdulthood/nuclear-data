# Test Data

The files in this directory consist of test input data and expected output
for the disassembler.

- `*.txt` hex dumps of test tape dump data
- `*.bin` binary equivalent of hex dumps
- `*.asm` expected output from the disassembler

To convert txt files to bin files:

```sh
xxd -r -p file.txt file.bin
```
