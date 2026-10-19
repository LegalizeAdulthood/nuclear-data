# Data Handling

This Nuclear Data assembly appears to be a four-slot-wide NIM module
containing acquisition and readout controls for a multichannel analyzer
system. The front panel is labeled `DATA HANDLING`, and the rear panel has
separate interfaces labeled `ADC`, `MEMORY`, `EXTERNAL`, `TYPEWRITER` and
`TELETYPE`. These markings support interpreting it as the control and
data-handling section of a larger analyzer system.

The identification and functional interpretation below are based on
physical inspection, the module photographs and comparison with Nuclear
Data documentation. The exact model, internal signal paths and interface
pinouts remain unresolved.

## Identification and construction

The manufacturer is identified on the rear panel as Nuclear Data, Inc.,
Schaumburg, Illinois. A handwritten side label appears to read `1100 DH`,
which is a possible lead for identifying the system family. The available
photographs do not establish the model number from the manufacturer's
`MODEL` field, so identification as a Series 1100 component remains
tentative.

The acquisition, grouping and readout functions also resemble those of the
**Series 3300 Data Handling Main Frame**, described in Nuclear Data
technical specifications reproduced in a
[NASA report](https://ntrs.nasa.gov/api/citations/19680006536/downloads/19680006536.pdf).
That is a comparative identification, not a confirmed model assignment. The
handwritten `1100 DH` label remains a separate identification lead; the
relationship between this unit and the 1100 or 3300 families needs a
matching manual or manufacturer part number.

The assembly contains multiple plug-in circuit boards. An internal rail
marks board positions 101 through 112, and the rear has both panel-mounted
connectors and attached cables. The card numbering alone does not identify
the system family or the functions of individual boards.

The rear photograph shows what appears to be the characteristic NIM bin
connector at the lower rear, and the front-panel proportions are consistent
with four NIM slots. The other multipin connectors and attached cables
serve the analyzer and peripheral interfaces; their presence does not
replace the apparent bin power connector. Power-rail requirements,
connector wiring and actual bin fit have not been verified.

## Relationship to the ND130 internal processor

The interfaces support interpreting this as a later, modular counterpart of
the [ND130 MCA's internal processor](../ND130/ND130.md). Here, processor
refers to the circuitry that coordinates spectrum-memory access, count
accumulation, arithmetic and readout. The ND130A manual describes its
corresponding subsystem as a count-tally computer and explains that the
same memory, adder and address circuitry serve both acquisition and
readout.

| Data Handling interface | Correspondence with the ND130 architecture |
| --- | --- |
| `TYPEWRITER` | The ND130A provides IBM output-typewriter solenoid drives and BCD digital readout for external recording devices. |
| `TELETYPE` | Fits the same digital spectrum-readout role, with another peripheral interface. The ND130A manual documents typewriter and tape interfaces; it does not establish this module's Teletype signaling. |
| `HORIZ` / `COM`, `VERT` / `COM` | Match the role of the ND130's analog spectrum readout: channel position determines horizontal deflection, while stored counts determine vertical deflection for a CRT or pen recorder. |
| `ADC`, `MEMORY` | Consistent with separating the conversion and spectrum-storage hardware from the tally, control and readout circuitry contained together in the ND130 analyzer. |

The front-panel acquisition/readout selection, grouping, add/subtract and
plot/display functions reinforce this functional continuity. Combined with
the confirmed absence of internal core memory, the interface set suggests
that this module packages the MCA's processing and readout functions while
using separate ADC and memory units. A direct circuit-level derivation from
the ND130, and compatibility with its interfaces, remain unverified.

See the
[ND130A instruction manual](../ND130/docs/512_Channel_Analyzer_Model_ND_130A_Instruction_Manual_26-May-1961.pdf),
particularly its readout controls and Digital Circuitry section (PDF pages
19-20 and 34; printed pages 17-18 and 32).

## Core memory

**This module contains no core memory.** This was confirmed by physical
inspection on 18 October 2026.

The rear connector labeled `MEMORY` reinforces the interpretation that
spectrum storage resides in a separate unit, with this module providing
acquisition and readout control. The required companion memory's type,
capacity and interface protocol remain unidentified.

## Acquisition and readout controls

The controls indicate several ways of collecting, storing and reading out
data. `PHA` conventionally denotes pulse-height analysis, and `MCS`
multichannel scaling. Their presence suggests that the assembly supports
both pulse-height spectra and sequences of counts taken over successive
time intervals. The distinction between its `MCS I` and `MCS II` modes, and
the behavior of the `EXT` selection, require documentation.

The following labels are visible in the front-panel photograph. Suggested
functions are interpretations of those labels, not verified operating
instructions.

| Control or indicator | Visible labels and interpretation |
| --- | --- |
| Acquisition selector | `PHA`, `MCS I`, `MCS II`, `EXT`; selects the acquisition function. Exact mode behavior remains unverified. |
| `MODE` | `ACQUIRE`, `STOP`, `REMOTE`, `READOUT`; local acquisition/readout state selection, with provision for remote operation. |
| Readout selector | `PLOT`, `TYPE`, `DISPLAY`, `XFER`, `READ-IN`; indicates support for several output destinations or transfer operations and for reading data into the system. |
| `MULTIPLIER` | `1`, `2`, `4`, `8`, `EXT`; the quantity being multiplied is not established by the label alone. |
| `GROUPS` | `12`, `1`, `2`, `O/LAP`, `EXT2`; suggests grouped-data selection or operation. The `12` marking and overlap behavior need a manual to interpret. |
| Time selector | `PHA SEC` markings of 10, 100, 1K, 10K and 100K; `MCS MSEC` markings of 0.1, 1, 10 and 100; also an infinity position. These indicate mode-dependent timing controls. |
| `COUNTS` | `100`, `400`, `1K`, `4K`, `10K`, `40K`, `100K`, `400K`, `1M`, `LOG`; consistent with a count-display scale control, including logarithmic display. Its exact role is unverified. |
| `ERASE` | `CH0`, `ALL`; indicates selectable erase operations. The scope of `CH0` must be checked before use. |
| `AUTO CYCLE` | `OFF`, `SNGL`, `REPEAT`; provides automatic-cycle selections. The sequence and stopping conditions are unknown. |
| `ADD` / `SUB` | Suggests accumulation or subtraction of data; exact behavior is unverified. |
| Status lamps | `ACQUIRE` and `READOUT`. |
| Analog meter | `PERCENT LOSSES`, with a 0-100 scale. The measured loss mechanism and calibration have not been established. |

The front-panel coaxial connectors are labeled `MCS COUNT`, `MCS START`,
`EXT CLOCK` and `SPARE`. The first three are consistent with external
count, start and clock signals for multichannel scaling. Their signal
direction, polarity, levels, impedance and timing requirements remain
unverified.

## Rear interfaces

The rear-panel photograph provides the clearest evidence of how the
assembly connects to the rest of an analyzer system.

| Marking | Observation and likely role |
| --- | --- |
| `MEMORY`, J11 | Multipin connector for a separate memory interface. The required companion memory's type, capacity and protocol are unknown. |
| `EXTERNAL`, J12 | Multipin external interface; its individual signals and remote-control functions have not been identified. |
| `ADC`, P1 | Label for an ADC connection among the attached cables; consistent with an external analog-to-digital converter supplying pulse-height information. |
| `TYPEWRITER`, P2; `TELETYPE`, P3 | Labels identify peripheral connections. They do not establish serial formats, electrical interfaces or connector pinouts. |
| `HORIZ`, `VERT`, each with `COM` | Consistent with horizontal and vertical analog display or plotting connections. Direction and voltage ranges remain unverified. |
| `COMPLETE`, `SEEK` | Labeled connections whose signaling functions remain unidentified. |
| `ROUTE 1`, J14; `ROUTE 2`, J15 | Two coaxial routing connections. The labels alone do not establish direction, encoding or their relationship to memory groups. |
| `512` / `256` | Two-position selector, possibly related to channel or memory configuration. Its actual function remains unverified. |
| `DSTR` / `OFF`; `PULSE` / `GATE` | Rear-panel switches. The meaning of `DSTR` and the function of pulse/gate selection require documentation. |

### Cable-end connectors

The two multipin cable ends use **AMP M Series rectangular pin-and-socket
connectors**, in different sizes. The listing photographs and
owner-supplied close-ups dated 18 October 2026 support the following
identification:

| Cable end | Contact housing | Metal shield / backshell |
| --- | --- | --- |
| Smaller blue connector | 20-position receptacle housing, marked **`200346-4`**. | Marked **`201227-2`**; short, straight-exit (180-degree) shield. |
| Larger black connector | 50-position male cable connector, with four staggered rows of 13, 12, 13 and 12 positions. The close-up appears to show 25 fitted pin contacts. The black phenolic plug housing matches **`201358-1`**, but that exact housing part number remains tentative because the complete molded marking has not been confirmed. | Marked **`201386-2`**; long, straight-exit (180-degree) shield with pin protection. |

The stamped numbers on the metal shields identify the **shields**, not the
complete connectors or their insulating contact housings. AMP's
[M Series catalog](https://www.te.com/content/dam/te-com/documents/appliances/global/m-series-datasheet.pdf)
lists the smaller housing and shield on printed pages 45 and 86, and the
50-position `201358-1` plug housing on printed page 47. The older
[1976 AMP Engineering and Purchasing Guide, section 16](https://www.bitsavers.org/components/amp/catalogs/1976_AMP_Engineering_and_Purchasing_Guide/1976_AMP_Engineering_and_Purchasing_Guide_16.pdf)
lists shield `201386-2` on printed page 16-45.

The different position counts distinguish the two cable-end connectors;
they are not interchangeable. These hardware identifications do not
establish the Nuclear Data signal assignments, pinouts or which cable end
corresponds to each rear-panel interface label.

## Working interpretation

Taken together, the panel controls and interfaces suggest an assembly that
coordinates acquisition, memory access, timing, display and peripheral
readout. In pulse-height operation, the separate ADC and memory connections
are consistent with receiving digitized pulse heights and accumulating a
spectrum in external memory. In multichannel-scaling operation, the count,
start and clock connectors are consistent with accumulating event counts
over a sequence of time bins. These are functional interpretations rather
than a traced circuit description.

The `GROUPS` and `ROUTE` markings suggest facilities for organizing or
routing data, but they do not establish compatibility with the
[ND588 analog multiplexer](ND588.md). This assembly's routing protocol,
gate semantics and connector compatibility remain unverified.

The Series 3300 comparison also distinguishes an **ADC Program Module**
from an actual ADC: the cited system architecture uses a control/interface
module with external ADC hardware. Thus the `ADC` interface on this Data
Handling assembly is consistent with its system-control role; it is not
evidence that one of its internal cards performs analog conversion. The
exact companion ADC and memory for the photographed unit remain unknown.

## Card extraction and inspection

The cards have circular holes in raised tabs at the accessible edges of the
cards. These are consistent with engagement points for a card extractor.
The boards were tightly seated during physical inspection.

A suitable extractor would engage a card and react against the cage rails,
applying a controlled pull along the insertion axis. Flotron's
[extractor definitions](https://flotron.com/extractor-and-inserters/)
describe a chassis-bearing bracket and a card-engaging pickup bar, both
customized for the application. Its
[extractor design sheet](https://flotron.com/wp-content/uploads/2014/11/extractor.pdf)
provides a reference for specifying the required geometry.

A bridge with a screw-driven, hole-engaging hook is one possible custom
design; it has not been tested on this module. Hole size, board thickness
and cage clearances need measurement before specifying an extractor. No
commercial tool has been confirmed as a direct fit.

## Remaining identification work

A manufacturer's manual or matching system diagram is needed to confirm the
model, required companion ADC and memory, power connections, and interface
pinouts. It would also need to explain the two MCS modes, group and routing
behavior, automatic cycles, loss meter and rear-panel switches. The
handwritten `1100 DH` label is a useful search lead, not sufficient
evidence to assign a model or copy another module's specifications.

## Sources

* Physical inspection on 18 October 2026: confirmed that this module
  contains no core memory.
* [AMP M Series pin-and-socket connector catalog](https://www.te.com/content/dam/te-com/documents/appliances/global/m-series-datasheet.pdf),
  printed pages 45, 47 and 86: housing and shield identifications for the
  smaller connector and the candidate housing for the larger connector.
* [1976 AMP Engineering and Purchasing Guide, section 16](https://www.bitsavers.org/components/amp/catalogs/1976_AMP_Engineering_and_Purchasing_Guide/1976_AMP_Engineering_and_Purchasing_Guide_16.pdf),
  printed page 16-45: shield `201386-2`, with straight cable exit and pin
  protection.
* [ND130A instruction manual](../ND130/docs/512_Channel_Analyzer_Model_ND_130A_Instruction_Manual_26-May-1961.pdf),
  describing the analyzer's internal tally computer, arithmetic, digital
  readout and analog display functions.
* [Nuclear Data Series 3300 specifications reproduced in a NASA report](https://ntrs.nasa.gov/api/citations/19680006536/downloads/19680006536.pdf),
  describing the Data Handling Main Frame, ADC Program Module and System
  Memory Unit. Its specifications have not been established as those of
  this particular module.
* [Flotron extractor definitions](https://flotron.com/extractor-and-inserters/)
  and
  [extractor design sheet](https://flotron.com/wp-content/uploads/2014/11/extractor.pdf),
  manufacturer references for chassis-supported extraction and custom
  card-engagement geometry.
* [Original Data Handling listing](https://www.ebay.com/itm/137242463917),
  source of the listing photographs below.
* [Front-panel photograph](images/Nuclear%20Data%20Data%20Handling%20137242463917-2.jpg),
  showing acquisition, timing, grouping and readout controls.
* [Side-label photograph](images/Nuclear%20Data%20Data%20Handling%20137242463917-3.jpg),
  showing the handwritten identification lead.
* [Internal photograph](images/Nuclear%20Data%20Data%20Handling%20137242463917-4.jpg),
  showing the plug-in boards and numbered positions.
* [Rear-panel photograph](images/Nuclear%20Data%20Data%20Handling%20137242463917-5.jpg),
  showing the manufacturer, interface names and switches.
* [Smaller cable-end photograph](images/Nuclear%20Data%20Data%20Handling%20137242463917-6.jpg),
  showing the `200346-4` housing and `201227-2` shield markings.
* [Larger cable-end photograph](images/Nuclear%20Data%20Data%20Handling%20137242463917-7.jpg),
  showing the larger housing, pin contacts and metal shield.

## Photographs

[![Data Handling](images/thumbs/Nuclear%20Data%20Data%20Handling%20137242463917-1.thumb.jpg)](images/Nuclear%20Data%20Data%20Handling%20137242463917-1.jpg)
[![Data Handling](images/thumbs/Nuclear%20Data%20Data%20Handling%20137242463917-2.thumb.jpg)](images/Nuclear%20Data%20Data%20Handling%20137242463917-2.jpg)
[![Data Handling](images/thumbs/Nuclear%20Data%20Data%20Handling%20137242463917-3.thumb.jpg)](images/Nuclear%20Data%20Data%20Handling%20137242463917-3.jpg)
[![Data Handling](images/thumbs/Nuclear%20Data%20Data%20Handling%20137242463917-4.thumb.jpg)](images/Nuclear%20Data%20Data%20Handling%20137242463917-4.jpg)
[![Data Handling](images/thumbs/Nuclear%20Data%20Data%20Handling%20137242463917-5.thumb.jpg)](images/Nuclear%20Data%20Data%20Handling%20137242463917-5.jpg)
[![Data Handling](images/thumbs/Nuclear%20Data%20Data%20Handling%20137242463917-6.thumb.jpg)](images/Nuclear%20Data%20Data%20Handling%20137242463917-6.jpg)
[![Data Handling](images/thumbs/Nuclear%20Data%20Data%20Handling%20137242463917-7.thumb.jpg)](images/Nuclear%20Data%20Data%20Handling%20137242463917-7.jpg)
