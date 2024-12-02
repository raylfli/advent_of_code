"""
Advent of Code 2024 - Day 1 Tests
"""

from solutions.d1 import solve_part1, solve_part2


class TestPart1:

    INPUT_STR = """3   4\n4   3\n2   5\n1   3\n3   9\n3   3\n"""

    def test_p1_1(self):
        assert solve_part1(self.INPUT_STR) == 11

    def test_p2_1(self):
        assert solve_part2(self.INPUT_STR) == 31
