"""
Advent of Code 2024 - Day 19 Tests
"""

from solutions.d19 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR_1 = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR_1) == 6


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR_1) == 16
