"""
Advent of Code 2024 - Day 8 Tests
"""

from solutions.d08 import solve_part1, solve_part2, compute_antinodes


class TestSuite:

    INPUT_STR = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


class TestPart1(TestSuite):

    def test_compute_antinodes_1(self):
        antennas = {
            (4, 3),
            (5, 5)
        }
        assert compute_antinodes(antennas, 9, 9) == {
            (3, 1),
            (6, 7)
        }

    def test_compute_antinodes_2(self):
        antennas = {
            (4, 3),
            (8, 4),
            (5, 5)
        }
        assert compute_antinodes(antennas, 9, 9) == {
            (3, 1),
            (0, 2),
            (2, 6),
            (6, 7)
        }

    def test_1(self):
        assert solve_part1(self.INPUT_STR) == 14


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR) == 34
