"""
Advent of Code 2024 - Runner Class
"""

import importlib


class Runner:
    """
    Class to run AoC solutions.
    """

    _day: int
    _part: int
    _input_path: str

    _input_str: str

    def __init__(self, day: int, part: int, input_path: str):
        self._day = int(day)
        self._part = int(part)
        self._input_path = str(input_path)

        with open(self._input_path) as f:
            self._input_str = f.read()

    def solve(self) -> int:
        """
        Run the solution.
        """
        mod = importlib.import_module(f'solutions.d{self._day}')
        if self._part == 1:
            return mod.solve_part1(self._input_str)
        else:
            return mod.solve_part2(self._input_str)
