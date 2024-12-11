"""
Advent of Code 2024 - Day 10 Tests
"""

from solutions.d10 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR) == 36


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR) == 81
