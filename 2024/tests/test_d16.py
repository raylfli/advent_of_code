"""
Advent of Code 2024 - Day 16 Tests
"""

from solutions.d16 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR_1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

    INPUT_STR_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR_1) == 7036

    def test_2(self):
        assert solve_part1(self.INPUT_STR_2) == 11048


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR_1) == 45

    def test_2(self):
        assert solve_part2(self.INPUT_STR_2) == 64
