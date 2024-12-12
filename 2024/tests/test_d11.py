"""
Advent of Code 2024 - Day 11 Tests
"""

from solutions.d11 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR = """125 17\n"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR) == 55312


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR) == 65601038650482
