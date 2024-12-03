"""
Advent of Code - Day 2: Red-Nosed Reports
"""

from itertools import pairwise


def _parse_reports(s: str) -> list[list[int]]:
    """
    Parse input string into row-based levels.
    """
    levels = []
    for row in s.strip().split('\n'):
        levels.append([int(n) for n in row.split(' ')])

    return levels


def _calculate_diffs(lst: list[int]) -> list[int]:
    """
    Calculate differences between pairwise elements.

    Returns a list of length `len(lst) - 1`.
    """
    return [b - a for a, b in pairwise(lst)]


def _ignore_level(diffs: list[int], i: int) -> None:
    """
    Ignore the level at index i by mutating diffs[i + 1].

    Does nothing if `i == len(diffs) - 1`.
    """
    if i != len(diffs) - 1:
        diffs[i + 1] += diffs[i]


def _check_diffs(diffs: list[int], tolerance: int = 0) -> bool:
    """
    Check differences of a report for level criteria.

    Tolerance indicates number of allowable dropped levels.
    """
    incr_flag = diffs[0] >= 0
    for d in diffs:
        if (
                d == 0
                or incr_flag and d < 0
                or not incr_flag and d > 0
                or abs(d) < 1
                or abs(d) > 3
        ):
            return False

    return True


def solve_part1(s: str) -> int:
    """
    Solve AoC D2 P1.
    """
    reports = _parse_reports(s)

    num_safe = 0
    for report in reports:
        diffs = _calculate_diffs(report)

        if _check_diffs(diffs):
            num_safe += 1

    return num_safe


def solve_part2(s: str) -> int:
    """
    Solve AoC D2 P2.
    """
    reports = _parse_reports(s)

    num_safe = 0
    for report in reports:
        if _check_diffs(_calculate_diffs(report)):
            num_safe += 1
        else:
            for i in range(len(report)):
                diffs = _calculate_diffs(report[:i] + report[i + 1:])

                if _check_diffs(diffs):
                    num_safe += 1
                    break

    return num_safe
