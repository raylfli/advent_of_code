"""
Advent of Code 2024 - Day 21 Tests
"""

from solutions.d21 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR_1 = """029A
980A
179A
456A
379A
"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR_1) == 126384


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR_1) == 154115708116294
