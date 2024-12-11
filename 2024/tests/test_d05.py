"""
Advent of Code 2024 - Day 5 Tests
"""

from solutions.d05 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR = """47|53\n97|13\n97|61\n97|47\n75|29\n61|13\n75|53\n29|13\n97|29\n53|29\n61|53\n97|53\n61|29\n47|13\n75|47\n97|75\n47|61\n75|61\n47|29\n75|13\n53|13\n\n75,47,61,53,29\n97,61,53,29,13\n75,29,13\n75,97,47,61,53\n61,13,29\n97,13,75,29,47\n"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR) == 143


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR) == 123
