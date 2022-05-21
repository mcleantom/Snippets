from Leetcode.BinarySearch.binary_search import solution
from unittest import TestCase


class Test(TestCase):

    def test_val_in_list(self):
        nums = [-1,0,3,5,9,12]
        target = 9
        self.assertEqual(4, solution(nums, target))

    def test_below_min(self):
        nums = [-1,0,3,5,9,12]
        target = -2
        self.assertEqual(-1, solution(nums, target))

    def test_above_max(self):
        nums = [-1, 0, 3, 5, 9, 12]
        target = 13
        self.assertEqual(-1, solution(nums, target))

    def test_one_item(self):
        nums = [5]
        target = 5
        self.assertEqual(0, solution(nums, target))