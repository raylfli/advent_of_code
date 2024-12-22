"""
Advent of Code 2024 - Day 22 Tests
"""

from solutions.d22 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR_1 = """1
10
100
2024
"""

    INPUT_STR_2 = """1
2
3
2024
"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR_1) == 37327623


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR_2) == 23
