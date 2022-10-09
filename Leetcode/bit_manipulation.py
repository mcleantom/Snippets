"""
&       - and
|       - or
~       - not
^       - exclusive-or (XOR)
<<, >>  - Bit shifting
"""
from collections import defaultdict


def count_one(n):
    """
    Count the number of ones in a binary representation of a number

    doing n-1 replaces the last 1 with a 0.
    doing n&(n-1) removes that last 1:

    count_one(456)
    ---
    0b111001000  n  &
    0b111000111  (n-1)
    0b111000000  =
    ---
    0b111000000
    0b110111111
    0b110000000
    ---
    0b110000000
    0b101111111
    0b100000000
    ---
    0b100000000
    0b11111111
    0b0

    """
    count = 0
    while (n):
        n = n & (n - 1)
        count += 1
    return count


# 456 -> 111001000
assert count_one(456) == 4


def is_power_of_four(n):
    """
    Return True if N is a power of 4

    A number is a power of 4 if:
        there is only one bit set (is a power of 2)
        The bits dont AND any part of the pattern 0xAAAAAAAA
        (0xAAAAAAAA is the bit representation of powers of 2 that are not of 4
        i.e. 2, 8, 32 etc.)
    """
    return (n != 0 and
            ((n & (n - 1)) == 0) and
            not (n & 0xAAAAAAAA))

assert is_power_of_four(64) == True
assert is_power_of_four(65) == False


def sum(a, b):
    """
    Sum two integers using bit manipulation.

    a^b finds where there is a 1 in either a, or b
    (a&b) finds where there is a 1 in both a and b
    (a&b) << 1 moves where there is a 1 in both a and b over by 1 (carry)

    repeat until there is no carry.
    """
    # 0b1111111111111111111111111111111
    MAX = 0x7FFFFFFF
    # 0b11111111111111111111111111111111
    MASK = 0xFFFFFFFF

    while b != 0:
        a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK

    return a if a <= MAX else ~(a ^ MASK)


assert sum(63, 63) == 63*2
assert sum(1, -2) == 1-2


def missing_number(nums):
    """
    Given an array of distinct ints from 0 to N, find the one that is
    missing from the array.

    XORing a number by its self, results in 0
        1^1 = 0
    XORing si commutative and associative
        (It doesnt matter what order it is applied)
    XORing by 0 results in the number, unchanged
        2^0 = 2

    We end up XORing every number twice, other than the missing number.
    """
    ret = len(nums)
    for i, num in enumerate(nums):
        ret ^= i
        ret ^= num
    return ret


assert missing_number([0,1,3,4,5]) == 2


def largest_power(N):
    """
    Find the largest power of 2, which is less than or equal to N

    We fill 1s from the most significant bit to the least significant bit
    by shifting the most significant bit to the right.

    then, we add 1 which sets all the 1s to 0, and the first 0 to 1.
    Then we shift the one back to the most significant bit's position.

    largest_power(33)
    ----
    bin(N)='0b100001'
    bin(N>>power)='0b10000'
    bin(N | N>>power)='0b110001'
    ----
    bin(N)='0b110001'
    bin(N>>power)='0b1100'
    bin(N | N>>power)='0b111101'
    ----
    bin(N)='0b111101'
    bin(N>>power)='0b11'
    bin(N | N>>power)='0b111111'
    ----
    bin(N)='0b111111'
    bin(N>>power)='0b0'
    bin(N | N>>power)='0b111111'
    ----
    bin(N)='0b111111'
    bin(N>>power)='0b0'
    bin(N | N>>power)='0b111111'
    ----
    bin(N)='0b111111'
    bin(N>>power)='0b0'
    bin(N | N>>power)='0b111111'
    ----
    bin(N+1>>1)='0b100000'
    """
    power = 1
    while power < N:
        N |= N >> power
        power = power << 1
    return (N+1) >> 1

assert largest_power(33) == 32


def largest_power_2(N):
    # if N is a power of 2, return it
    if not (N&(N-1)):
        return N

    # Else, set only the most significant bit
    # The hex is a 1, followed by 64 zeros.
    return 0x8000000000000000 >> (64-N.bit_length())


assert largest_power_2(33) == 32


def hamming_weight(n):
    """
    n&(n-1) replaces the last 1 with a 0
    repeat until all 1s are removed.
    """
    count = 0
    while n:
        n = n&(n-1)
        count += 1
    return count


assert hamming_weight(10) == count_one(10)


def count_bits(N):
    """
    Whole numbers can be represented by 2N (even) or 2N+1 (odd)
    For a binary number, multiplying by 2 is the same as adding a 0 to the end.
    Therefore, a number and its double will have the same number of 1s.
    Doubling a number and adding 1 will increase the count by 1

    count_bits(N) = count_bits(2N)
    count_bits(N)+1 = count_bits(2N+1)
    """
    n_bits = [0]*(N+1)

    for i in range(N+1):
        n_bits[i] = n_bits[i//2] + i % 2

    return n_bits


assert count_bits(5) == [0, 1, 1, 2, 1, 2]


def reverseBits(n):
    res = 0
    for i in range(31, -1, -1):
        if n & (1 << i):
            res += 1 << (31 - i)
    return res


assert reverseBits(0b11111111111111111111111111111101) == 0b10111111111111111111111111111111