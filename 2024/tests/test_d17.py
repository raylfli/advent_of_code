"""
Advent of Code 2024 - Day 17 Tests
"""

from solutions.d17 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR_1 = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

    INPUT_STR_2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR_1) == "4,6,3,5,6,3,5,2,1,0"


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR_2, parallel=False) == 117440
