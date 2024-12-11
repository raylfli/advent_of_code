"""
Advent of Code 2024 - Day 6 Tests
"""

from solutions.d06 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR = """....#.....\n.........#\n..........\n..#.......\n.......#..\n..........\n.#..^.....\n........#.\n#.........\n......#...\n"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR) == 41


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR) == 6
