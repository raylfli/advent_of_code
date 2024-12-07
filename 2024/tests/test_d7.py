"""
Advent of Code 2024 - Day 7 Tests
"""

from solutions.d7 import solve_part1, solve_part2, check_equation


class TestSuite:

    INPUT_STR = """190: 10 19\n3267: 81 40 27\n83: 17 5\n156: 15 6\n7290: 6 8 6 15\n161011: 16 10 13\n192: 17 8 14\n21037: 9 7 18 13\n292: 11 6 16 20\n"""


class TestPart1(TestSuite):

    def test_check_equation_true_1(self):
        assert check_equation(1, (1,))

    def test_check_equation_true_2(self):
        assert check_equation(190, (10, 19))

    def test_check_equation_true_3(self):
        assert check_equation(10, (3, 7))

    def test_1(self):
        assert solve_part1(self.INPUT_STR) == 3749


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR) == 11387
