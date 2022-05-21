from Leetcode.kth_symbol_in_grammar.solution import kthGrammar
from unittest import TestCase


class KthSymbol(TestCase):

    def test_simple(self):
        self.assertEqual(0, kthGrammar(1, 1))

    def test_multi(self):
        self.assertEqual(1, kthGrammar(2, 2))

    def test_long(self):
        self.assertEqual(1, kthGrammar(10,10))