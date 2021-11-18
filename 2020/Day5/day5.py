""" ADVENT OF CODE 2020 - DAY 5 - RAYMOND LI """

from __future__ import annotations

from typing import List


def read_input(filepath: str) -> List[int]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        seats = input_file.read().strip().split('\n')

    ids = []
    for seat in seats:
        upper_row = 128
        lower_row = 1
        for row_split in seat[:7]:
            if row_split == 'F':
                upper_row = (upper_row - lower_row) // 2 + lower_row
            elif row_split == 'B':
                lower_row = upper_row - (upper_row - lower_row) // 2

        upper_col = 8
        lower_col = 1
        for col_split in seat[-3:]:
            if col_split == 'L':
                upper_col = (upper_col - lower_col) // 2 + lower_col
            elif col_split == 'R':
                lower_col = upper_col - (upper_col - lower_col) // 2

        ids.append((upper_row - 1) * 8 + (upper_col - 1))

    return ids


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 5 Part 1 problem.
    """
    ids = read_input(filepath)

    return max(ids)


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 5 Part 2 problem.
    """
    ids = read_input(filepath)

    ids.sort()
    min_id = ids[0]
    for i in range(len(ids)):
        if min_id + i != ids[i]:
            return ids[i] - 1

    return -1


if __name__ == '__main__':
    print(f'D5P1: {solve_part1("input.txt")}')
    print(f'D5P2: {solve_part2("input.txt")}')
