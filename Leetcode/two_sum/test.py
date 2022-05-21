from unittest import TestCase
from .solution import Solution


class TestSolution(TestCase):

    def test_two_sum(self):
        solver = Solution()

        nums = [2, 7, 11, 15]
        target = 9
        expected = [0, 1]

        self.assertEqual(solver.twoSum(nums, target), expected)

        nums = [3,2,4]
        target = 6
        expected = [1, 2]

        self.assertEqual(solver.twoSum(nums, target), expected)

        nums = [3, 3]
        target = 6
        expected = [0, 1]

        self.assertEqual(solver.twoSum(nums, target), expected)