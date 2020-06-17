'''
Bitwise operations
~ - bitwise NOT ex: ~x
& - bitwist AND ex: x & y
| - bitwise OR ex: x | y
~(&) - bitwise NAND (not AND): (AND inverted), when ONE is true or NONE is true ex: ~(x & y)
~(|) - bitwise NOR (not OR): (OR inverted), when neither are true ex: ~(x | y)
^ - bitwise XOR (exclusive OR): when only one is true ex: x ^ y
# Multi-bit numbers - Do operation bit by bit
    11101011    1 - true
&   10011101    1 - true
--------------------------
    10001001    1 - true AND true = true, so 1
    11011010
^   11100011
--------------
    00111001
# AND operations as a mask
    11010110
&   11110000 - ANDing a bitwith 1 will give you the bit's value, ANDing it with 0, will give you 0
--------------
    11010000
# shifting bitwise numbers - << and >>
     1111
<<1 11110 - fills in 0s for new bits
    1111
>>1  111 - removes last bit, other bits shift right.
'''
