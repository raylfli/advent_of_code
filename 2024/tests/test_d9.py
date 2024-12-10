"""
Advent of Code 2024 - Day 9 Tests
"""

from solutions.d9 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR = """2333133121414131402"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR) == 1928


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR) == 2858
