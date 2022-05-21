from unittest import TestCase
from .solution import Solution


class TestSolution(TestCase):

    def test_two_sum(self):
        solver = Solution()

        nums = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
        expected = 7

        self.assertEqual(expected, solver.minPathSum(nums))

        nums = [[1, 2, 3], [4, 5, 6]]
        expected = 12

        self.assertEqual(expected, solver.minPathSum(nums))