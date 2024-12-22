"""
Advent of Code 2024 - Day 20 Tests
"""

from solutions.d20 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR_1 = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR_1, time_save=2) == 14 + 14 + 2 + 4 + 2 + 3 + (
            1 * 5
        )


class TestPart2(TestSuite):

    def test_1(self):
        assert (
            solve_part2(self.INPUT_STR_1, time_save=50)
            == 32 + 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
        )
