"""
Advent of Code 2024 - Day 18 Tests
"""

from solutions.d18 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR_1 = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR_1, mem_size=6, num_locations=12) == 22


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR_1, mem_size=6) == (6, 1)
