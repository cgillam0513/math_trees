#!/usr/bin/env python

import unittest

from math_trees.math_trees import parse_str, eval_expr


class TestMathTrees(unittest.TestCase):
    def test_basic_string(self):
        math_string = "3 + 4 * 2"
        math_tree = parse_str(math_string)
        value = eval_expr(math_tree)
        self.assertEqual(value, 11)

    def test_another_string(self):
        math_string = "8 - 9 / 3"
        math_tree = parse_str(math_string)
        value = eval_expr(math_tree)
        self.assertEqual(value, 5)

    def test3(self):
        math_string = "8.2 + 9.8 - 3.2"
        math_tree = parse_str(math_string)
        value = eval_expr(math_tree)
        self.assertEqual(value, 14.8)

    def test4(self):
        math_string = "3*(2+4)-6"
        math_tree = parse_str(math_string)
        value = eval_expr(math_tree)
        self.assertEqual(value, 12)

    def test5(self):
        math_string = "3*(2+(4-6)-3)*9+5"
        math_tree = parse_str(math_string)
        value = eval_expr(math_tree)
        self.assertEqual(value, -76)

    def test6(self):
        math_string = "3(2+(4-6)-3)*9+5"
        math_tree = parse_str(math_string)
        value = eval_expr(math_tree)
        self.assertEqual(value, -76)

    def test7(self):
        math_string = "3*7/7(1+4)"
        math_tree = parse_str(math_string)
        value = eval_expr(math_tree)
        self.assertEqual(value, 15.0)
