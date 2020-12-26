""" ADVENT OF CODE 2020 - DAY 1 - RAYMOND LI """

from __future__ import annotations

from typing import List


def read_input(filepath: str) -> List[int]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        return [int(line) for line in input_file.read().split()]


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 1 Part 1 problem.
    """
    nums = read_input(filepath)

    for a in nums:
        for b in nums:
            if a + b == 2020:
                return a * b

    return -1


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 1 Part 2 problem.
    """
    nums = read_input(filepath)

    for a in nums:
        for b in nums:
            for c in nums:
                if a + b + c == 2020:
                    return a * b * c

    return -1


if __name__ == '__main__':
    print(f'D1P1: {solve_part1("input.txt")}')
    print(f'D1P2: {solve_part2("input.txt")}')
