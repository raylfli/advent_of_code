"""
Advent of Code - Day 4: Ceres Search
"""


def _is_xmas(puzzle: list[str], row: int, col: int, drow: int, dcol: int) -> bool:
    """
    Check if XMAS is present in the puzzle rooted at
    the specified (row, col) and in the (drow, dcol) direction.
    """
    row -= drow
    col -= dcol
    for c in "XMAS":
        row += drow
        col += dcol
        if (
            0 <= row < len(puzzle)
            and 0 <= col < len(puzzle[0])
            and puzzle[row][col] == c
        ):
            continue
        else:
            return False

    return True


def _find_xmas(puzzle: list[str], row: int, col: int) -> int:
    """
    Return the number of XMAS instances around the given row and cell.
    """
    DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    total = 0
    for dr, dc in DIRECTIONS:
        if _is_xmas(puzzle, row, col, dr, dc):
            total += 1

    return total


def _check_x_mas(puzzle: list[str], row: int, col: int) -> bool:
    """
    Return whether (row, col) is the centre of an X-MAS.
    """
    if row == 0 or row == len(puzzle) - 1 or col == 0 or col == len(puzzle[0]) - 1:
        return False

    pos_diag = {puzzle[row + 1][col - 1], puzzle[row - 1][col + 1]}
    neg_diag = {puzzle[row - 1][col - 1], puzzle[row + 1][col + 1]}

    return {"M", "S"} == pos_diag == neg_diag


def solve_part1(s: str) -> int:
    """
    Solve AoC D4 P1.
    """
    puzzle = [row.strip() for row in s.strip().split("\n")]

    total = 0
    for r, row in enumerate(puzzle):
        for c, cell in enumerate(row):
            if cell == "X":
                total += _find_xmas(puzzle, r, c)

    return total


def solve_part2(s: str) -> int:
    """
    Solve AoC D4 P2.
    """
    puzzle = [row.strip() for row in s.strip().split("\n")]

    total = 0
    for r, row in enumerate(puzzle):
        for c, cell in enumerate(row):
            if cell == "A":
                if _check_x_mas(puzzle, r, c):
                    total += 1

    return total
