#!/usr/bin/env python

# Pearson Coding Challenge Tests
# Author: Christopher Gillam
# Date: 10/01/2021

import unittest

from math_trees.math_trees import parse_str


class TestMathTrees(unittest.TestCase):
    def test_basic_string(self):
        math_string = "3 + 4 * 2"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, 11)

    def test_another_string(self):
        math_string = "8 - 9 / 3"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, 5)

    def test3(self):
        math_string = "8.2 + 9.8 - 3.2"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, 14.8)

    def test4(self):
        math_string = "3*(2+4)-6"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, 12)

    def test5(self):
        math_string = "3*(2+(4-6)-3)*9+5"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, -76)

    def test6(self):
        math_string = "3(2+(4-6)-3)*9+5"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, -76)

    def test7(self):
        math_string = "3*7/7(1+4)"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, 15.0)

    def test8(self):
        math_string = "3*+4"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, 12)

    def test9(self):
        math_string = "3*-4"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, -12)

    def test10(self):
        math_string = ".3+.5"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, 0.8)

    def test11(self):
        math_string = "-.3+-0.5"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, -0.8)

    def test12(self):
        math_string = "0.3+0.5"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, 0.8)

    def test13(self):
        math_string = "-0.3+-0.5"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, -0.8)

    def test14(self):
        math_string = "+0.3++0.5"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, 0.8)

    def test15(self):
        math_string = "+.3++.5"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, 0.8)

    def test16(self):
        math_string = "00000123"
        math_tree = parse_str(math_string)
        value = math_tree.eval()
        self.assertEqual(value, 123)

    def test17(self):
        math_string = "3(2+(4-6)-3)*9+5"
        math_tree = parse_str(math_string)
        s = str(math_tree)
        self.assertEqual(s, '3*(2+(4-6)-3)*9+5')
