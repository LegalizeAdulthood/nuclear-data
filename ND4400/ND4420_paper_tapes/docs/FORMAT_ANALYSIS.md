# ND4400/ND4420 Paper Tape Format Analysis

## Summary

The ND4400/ND4420 paper tape files use a **hybrid format** that combines:
1. **Standard ND812 binary records** (executable code/data)
2. **Unknown data sections** (purpose unclear - not readable text)

## Format Structure

### Overall Layout
```
[NUL Leader] [0x80 Leader] [Mixed Records and Text] [0x80 Trailer (optional)]
```

### Components

#### 1. Leader Section
- **NUL bytes**: Variable length (53-130 bytes observed)
- **0x80 bytes**: Typically 128 bytes
- These are skipped during loading

#### 2. Binary Records
Standard ND812 paper tape format:
- **Field change** (optional): `0x84-0x87` (bits select field 0-3)
- **Origin address**: 2 bytes
  - First byte: Has `0x40` bit set (marked byte)
  - Second byte: Plain 6-bit value
  - Address = `((byte1 & 0x3F) << 6) | (byte2 & 0x3F)`
- **Payload**: Pairs of 6-bit bytes forming 12-bit words
  - Each byte is `0x00-0x3F` (unmarked)
- **Checksum**: 2 bytes (first has `0x40` bit set)
- **Empty records**: Some records have origin + checksum only (no payload)

#### 3. Unknown Data Sections
Between binary records, there are sections of **unmarked 6-bit data**:
- Bytes without the `0x40` marker bit (values 0x00-0x3F)
- Not part of any record structure
- **Purpose unclear** - attempts to decode as packed ASCII produce unreadable output
- Lengths vary from 22 to 5,816 bytes
- Possible purposes (unconfirmed):
  - Compressed or encoded data
  - Symbol tables or relocation information
  - Data in a proprietary format
  - Overlay metadata for loader
  - Padding or alignment data

**Identifying Unknown Data Sections:**

The pattern is very consistent and can be reliably detected:

**Start marker:**
- Immediately follows a checksum (2-byte marked record ending)
- Next byte is **unmarked** (0x00-0x3F)
- Next byte is **NOT** 0x80 (leader byte)
- Next byte is **NOT** a field change (0x84-0x87)

**End marker:**
- Next **marked** byte (0x40-0x7F) appears -> start of next record's origin
- OR next **field change** byte (0x84-0x87) appears

**Detection Algorithm:**
```python
# After reading checksum:
if next_byte < 0x40 and next_byte != 0x80 and not (0x84 <= next_byte <= 0x87):
    # Start of unknown data section
    while next_byte < 0x40 and not (0x84 <= next_byte <= 0x87):
        # Skip unknown data
        next_byte = read_byte()
    # Now at start of next record or field change
```

This makes it straightforward for the disassembler to skip these sections.

The high frequency of 0x00 bytes (17.89%) initially suggested text (spaces), but decoding attempts using the ND812 packed ASCII character table (CharacterEncoding.md) produce gibberish rather than readable source code.

### Example from ND41-1061-00
```
Offset  Content                 Interpretation
------  -----------------------  --------------------------
0x000   [53 NUL bytes]          Leader padding
0x035   [128 0x80 bytes]        Leader
0x0B5   0x41 0x00               Record 1: Origin = 0100
0x0B7   0x40 0x21               Checksum = 0041 (empty record)
0x0B9   [32 unmarked bytes]     Unknown data section
0x0D9   0x40 0x31               Record 2: Origin...
...
```

## Statistics Across All Files

| File | Records | Payload Bytes | Unknown Bytes |
|:-----|--------:|--------------:|-----------:|
| ND41-1061-00 | 10 | 1,080 | 350 |
| ND41-1062-00 | 10 | 1,064 | 415 |
| ND41-1076-01 | 6 | 694 | 1,104 |
| ND41-1076-02 PART1 | 8 | 5,600 | 334 |
| ND41-1076-02 PART2 | 4 | 2,366 | 128 |
| ND41-1076-02 PART3 | 6 | 294 | 5,748 |
| ND41-1076-02 PART4B | 7 | 660 | 1,150 |
| ND41-1085-00 | 8 | 3,718 | 442 |
| ND41-1101-02 | 2 | 178 | 3,024 |
| ND41-1102-03 | 4 | 620 | 846 |
| ND41-1104-00 | 15 | 2,060 | 5,688 |
| ND41-1105-01 | 9 | 1,096 | 475 |
| ND41-1108-00 | 7 | 4,422 | 3,313 |
| ND41-5032-00 | 2 | 178 | 602 |
| ND41-6001-02 | 4 | 1,170 | 5,816 |
| ND41-6012-00 | 6 | 1,106 | 6,401 |
| ORCAL6-8K-LC02 | 3 | 4,264 | 3,344 |

## Key Differences from ND812 Test Files

1. **Interleaved Unknown Data**: ND4400 files contain unmarked data sections between binary records
2. **Empty Records**: Some files have records with only origin + checksum (no payload)
3. **Checksum Algorithm**: May differ (mismatches observed on empty records)
4. **Purpose**: Unknown - possibly overlay files with proprietary metadata format

## Implications for Disassembler

The current `disassemble.py` script needs modifications to handle:

1. **Unknown data sections**: Recognize and skip/dump unmarked data bytes between records
2. **Empty records**: Handle records with no payload gracefully
3. **Mixed content**: Distinguish between executable code and unknown data sections
4. **Output format**: Option to display, skip, or hex-dump unknown data sections

## Recommendations

1. **Skip unknown data**: When disassembling, skip over unknown data sections to show only code
2. **Hex dump option**: Add option to hex-dump unknown data sections for analysis
3. **Further research**: Investigate ND4400 documentation to determine data section format
4. **Conservative approach**: Treat as opaque binary data unless format is documented

## Disassembler Status

The ND812 disassembler has been updated to handle **NUL bytes between records**, which is a common pattern in ND4400/ND4420 files. This allows it to process files that use NUL padding between records.

**Test case added:**
- `ND812/scripts/test/nul-bytes.bin` - Contains two valid records with 11 NUL bytes between them
- Disassembler now skips both 0x80 (leader) and 0x00 (NUL) bytes after each record's checksum

**Remaining work:**
- Implement full unknown data section detection and skipping (using the algorithm in this document)
- This will allow disassembling the binary records in ND4400 files while skipping the unknown data sections

## Notes

- These files contain both binary records AND unknown data sections
- The unknown data does NOT decode to readable text using standard packed ASCII
- Format may be proprietary to ND4400/ND4420 or specific to these programs
- Further research needed to determine the purpose and format of unknown sections
- The high percentage of 0x00 bytes may indicate padding, null values, or data structure alignment

---

## Unknown Data Sections

The unmarked bytes between binary records contain data of **unknown purpose and format**.

### Histogram Analysis

Analyzing all 39,180 bytes from unknown data sections across 17 files reveals:

**Top 10 Most Common Byte Values:**
1. `0x00` (17.89%) - Most common value (NULL/padding?)
2. `0x06` (3.37%)
3. `0x0D` (3.24%)
4. `0x20` (3.23%)
5. `0x80` (3.06%) - **Invalid 6-bit value** (has bit 7 set) - likely leader bytes
6. `0x05` (2.95%)
7. `0x39` (2.94%)
8. `0x02` (2.37%)
9. `0x0C` (2.11%)
10. `0x01` (2.10%)

**Key Observations:**
- Distribution is NOT uniform (not random/encrypted data)
- High frequency of 0x00 (17.89%) suggests padding or null values
- Attempts to decode as packed ASCII (using CharacterEncoding.md) produce unreadable gibberish
- When interpreted as 12-bit instruction word pairs, some appear to be valid ND812 instructions
- No clear pattern emerges from analysis

**Attempted Interpretations:**
1. **Packed ASCII text** - FAILED: produces gibberish like `%@4P &@3OL 'M-$ .?19F`
2. **Raw ASCII** - FAILED: no readable text patterns
3. **Instruction pairs** - PARTIAL: some decode to valid instructions, but many don't
4. **Data tables** - POSSIBLE: but structure is unclear

**Conclusion:** The format and purpose of these data sections remains **UNKNOWN**. They are not:
- Readable source code
- Standard packed ASCII text
- Pure machine instructions
- Random padding

Further research into ND4400/ND4420 documentation is needed to determine the actual format.

