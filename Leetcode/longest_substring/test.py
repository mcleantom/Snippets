from unittest import TestCase
from .solution import Solution

class TestLongestString(TestCase):
    def test_1(self):
        self.assertEqual(Solution().lengthOfLongestSubstring("abcabcbb"), 3)