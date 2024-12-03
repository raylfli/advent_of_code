"""
Advent of Code 2024 - Day 1 Tests
"""

from solutions.d1 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR = """3   4\n4   3\n2   5\n1   3\n3   9\n3   3\n"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR) == 11


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR) == 31
