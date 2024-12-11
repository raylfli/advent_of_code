"""
Advent of Code 2024 - Day 3 Tests
"""

from solutions.d03 import solve_part1, solve_part2


class TestSuite:

    pass


class TestPart1(TestSuite):

    INPUT_STR = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))\n"""

    def test_1(self):
        assert solve_part1(self.INPUT_STR) == 161


class TestPart2(TestSuite):

    INPUT_STR = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))\n"""

    def test_1(self):
        assert solve_part2(self.INPUT_STR) == 48
