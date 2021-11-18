""" ADVENT OF CODE 2020 - DAY 3 - RAYMOND LI """

from __future__ import annotations

from math import prod
from typing import List


def read_input(filepath: str) -> List[str]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        return input_file.read().strip().split('\n')


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 3 Part 1 problem.
    """
    rows = read_input(filepath)

    trees = 0
    col_num = 0
    for row_num in range(len(rows)):
        if rows[row_num][col_num % len(rows[row_num])] == '#':
            trees += 1

        col_num += 3

    return trees


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 3 Part 2 problem.
    """
    rows = read_input(filepath)

    trees = []

    # Tuple[int, int]: (right movement, down movement)
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    for slope in slopes:
        tree_count = 0
        col_num = 0
        row_num = 0
        while row_num < len(rows):
            if rows[row_num][col_num % len(rows[row_num])] == '#':
                tree_count += 1

            col_num += slope[0]
            row_num += slope[1]

        trees.append(tree_count)

    return prod(trees)


if __name__ == '__main__':
    print(f'D3P1: {solve_part1("input.txt")}')
    print(f'D3P2: {solve_part2("input.txt")}')
