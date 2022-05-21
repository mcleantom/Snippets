from Leetcode.DynamicProgramming.fibonacci_number.fibonacci_number import fib
from unittest import TestCase


class Fibonacci(TestCase):

    def test_fib_2(self):
        self.assertEqual(1, fib(2))

    def test_fib_3(self):
        self.assertEqual(2, fib(3))

    def test_fib_4(self):
        self.assertEqual(3, fib(4))