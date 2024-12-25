"""
Advent of Code 2024 - Day 25 Tests
"""

from solutions.d25 import solve_part1


class TestSuite:

    INPUT_STR_1 = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR_1) == 3


class TestPart2(TestSuite):

    def test_1(self):
        # no part 2!
        # it is always a star gate
        assert True
