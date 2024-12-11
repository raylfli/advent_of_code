"""
Advent of Code 2024 - Day 2 Tests
"""

from solutions.d02 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR = """7 6 4 2 1\n9 7 6 2 1\n1 2 7 8 9\n1 3 2 4 5\n8 6 4 4 1\n1 3 6 7 9\n"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR) == 2


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR) == 4
