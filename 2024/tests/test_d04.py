"""
Advent of Code 2024 - Day 4 Tests
"""

from solutions.d04 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR_1 = """..X...\n.SAMX.\n.A..A.\nXMAS.S\n.X....\n"""
    INPUT_STR_2 = """MMMSXXMASM\nMSAMXMSMSA\nAMXSXMAAMM\nMSAMASMSMX\nXMASAMXAMM\nXXAMMXXAMA\nSMSMSASXSS\nSAXAMASAAA\nMAMMMXMMMM\nMXMXAXMASX\n"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR_1) == 4

    def test_2(self):
        assert solve_part1(self.INPUT_STR_2) == 18


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR_2) == 9
