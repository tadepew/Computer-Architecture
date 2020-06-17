## Bitwise Operations Tuesday - 06/16/2020

- Binary representations of booleans
- `~` = Not (in C)
- `NOT` Truth Table:
  |A|Not A|
  |:---|:---|
  |0|1|
  |1|0|
- `AND` Truth Table:
  |A|B|A `&` B|
  |:---|:---|:--|
  |0|0|0|
  |1|0|0|
  |0|1|0|
  |1|1|1|
  - both on
- `OR` Truth Table:
  |A|B|A `|` B|
  |:---|:---|:--|
  |0|0|0|
  |1|0|1|
  |0|1|1|
  |1|1|1|
- `NAND` Truth Table:
  |A|B|A `!&` B|
  |:---|:---|:--|
  |0|0|1|
  |1|0|1|
  |0|1|1|
  |1|1|0|
  - inverse AND
- `NOR` Truth Table:
  |A|B|A `!|` B|
  |:---|:---|:--|
  |0|0|1|
  |1|0|0|
  |0|1|0|
  |1|1|0|
  - inverse OR
- `XOR` Truth Table:
  |A|B|A `^` B|
  |:---|:---|:--|
  |0|0|1|
  |1|0|0|
  |0|1|0|
  |1|1|1|
  - both on and both off (&^2)
