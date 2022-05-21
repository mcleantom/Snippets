from ..solution import LIS
from unittest import TestCase


class TestLIS(TestCase):

    def test_1(self):
        a = [3, 1, 8, 2, 5]
        self.assertEqual(3, LIS(a))

    def test_2(self):
        a = [5, 2, 8, 6, 3, 6, 8, 5]
        self.assertEqual(4, LIS(a))

def goldenLeader(A):
    n = len(A)
    size = 0
    for k in range(n):
        if size == 0:
            size += 1
            value = A[k]
        else:
            if (value != A[k]):
                size -= 1
            else:
                size += 1
    candidate = -1
    if (size > 0):
        candidate = value
    leader = -1
    count = 0
    for k in range(n):
        if (A[k] == candidate):
            count += 1
    if (count > n // 2):
        leader = candidate
    return leader