"""
Advent of Code 2024 - Day 14 Tests
"""

from solutions.d14 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR, space_size=(11, 7)) == 12


class TestPart2(TestSuite):

    def test_1(self):
        # there is no test case here
        assert True
