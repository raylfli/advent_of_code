"""
Advent of Code - Day 22: Monkey Market
"""

from collections import defaultdict
from itertools import pairwise


def _parse_input(s: str) -> list[int]:
    """
    Parse input into list of initial secret numbers.
    """
    return [int(n) for n in s.strip().split("\n")]


def _step_secret_number(n: int) -> int:
    """
    Generate the next secret number.
    """
    # first step
    mult = n << 6  # multiply by 64
    n ^= mult
    n &= 0b111111111111111111111111  # % 16777216, log_2(16777216) == 24

    # second step
    divided = n >> 5
    n ^= divided
    n &= 0b111111111111111111111111

    # third step
    mult = n << 11
    n ^= mult
    n &= 0b111111111111111111111111
    return n


def _find_patterns_and_prices(
    prices: list[int], changes: list[int]
) -> dict[tuple[int, int, int, int], int]:
    """
    Find the first price for every unique sequence of changes.

    Assumptions:
    - len(prices) - 1 == len(changes)
    """
    patt_prices = {}
    for i in range(len(changes) - 3):
        patt = (changes[i], changes[i + 1], changes[i + 2], changes[i + 3])
        if patt not in patt_prices:
            patt_prices[patt] = prices[i + 4]
    return patt_prices


def solve_part1(s: str) -> int:
    """
    Solve AoC D22 P1.
    """
    initials = _parse_input(s)

    total = 0
    for initial in initials:
        n = initial
        for _ in range(2000):
            n = _step_secret_number(n)
        total += n
    return total


def solve_part2(s: str) -> int:
    """
    Solve AoC D22 P2.
    """
    initials = _parse_input(s)

    # get all buyer prices
    prices = []
    changes = []

    for initial in initials:
        prices.append([])
        n = initial
        for _ in range(2000):
            n = _step_secret_number(n)
            prices[-1].append(n % 10)

        changes.append([])
        for a, b in pairwise(prices[-1]):
            changes[-1].append(b - a)

    # find all patterns for each buyer
    patt_values = defaultdict(lambda: 0)
    for ps, cs in zip(prices, changes):
        patt_prices = _find_patterns_and_prices(ps, cs)
        for patt, price in patt_prices.items():
            patt_values[patt] += price
    return max(patt_values.values())
