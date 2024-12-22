"""
Advent of Code - Day 19: Linen Layout
"""

from functools import cache


def _parse_towels(s: str) -> list[str]:
    """
    Parse list of towels.
    """
    return s.strip().split(", ")


def _parse_patterns(s: str) -> list[str]:
    """
    Parse list of patterns.
    """
    return s.strip().split("\n")


def _parse_input(s: str) -> tuple[list[str], list[str]]:
    """
    Parse input into list of available towels and desired towel patterns.
    """
    towels, patterns = s.strip().split("\n\n")
    return _parse_towels(towels), _parse_patterns(patterns)


@cache
def _make_pattern(towels: tuple[str, ...], pattern: str) -> int:
    """
    Return the number of ways a pattern can be made with the given towels.
    """
    num_ways = 0
    for towel in towels:
        if len(towel) > len(pattern):
            continue
        if towel == pattern:
            num_ways += 1
            continue
        if len(towel) == len(pattern):
            continue
        if pattern.startswith(towel):
            ret = _make_pattern(towels, pattern[len(towel) :])
            if ret > 0:
                num_ways += ret

    return num_ways


def solve_part1(s: str) -> int:
    """
    Solve AoC D19 P1.
    """
    towels, patterns = _parse_input(s)
    towels.sort(reverse=True)

    towel_tup = tuple(towels)

    total = 0
    for patt in patterns:
        if _make_pattern(towel_tup, patt) > 0:
            total += 1
    return total


def solve_part2(s: str) -> int:
    """
    Solve AoC D19 P2.
    """
    towels, patterns = _parse_input(s)
    towels.sort(reverse=True)

    towel_tup = tuple(towels)

    total = 0
    for patt in patterns:
        num_ways = _make_pattern(towel_tup, patt)
        total += num_ways
    return total
