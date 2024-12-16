"""
Advent of Code 2024 - Day 12 Tests
"""

from solutions.d12 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR_1 = """AAAA
BBCD
BBCC
EEEC
"""

    INPUT_STR_2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

    INPUT_STR_3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR_1) == 140

    def test_2(self):
        assert solve_part1(self.INPUT_STR_2) == 772

    def test_3(self):
        assert solve_part1(self.INPUT_STR_3) == 1930


class TestPart2(TestSuite):

    INPUT_STR_4 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""

    INPUT_STR_5 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""

    def test_1(self):
        assert solve_part2(self.INPUT_STR_1) == 80

    def test_2(self):
        assert solve_part2(self.INPUT_STR_2) == 436

    def test_3(self):
        assert solve_part2(self.INPUT_STR_3) == 1206

    def test_4(self):
        assert solve_part2(self.INPUT_STR_4) == 236

    def test_5(self):
        assert solve_part2(self.INPUT_STR_5) == 368
