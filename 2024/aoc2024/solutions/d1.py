"""
Advent of Code - Day 1: Historian Hysteria
"""

from collections import Counter


def _parse_two_list(s: str) -> (list[int], list[int]):
    """
    Parse input string into two lists.
    """
    l1, l2 = [], []
    for line in s.strip().split('\n'):
        left, right = line.split('   ', maxsplit=1)
        l1.append(int(left))
        l2.append(int(right))

    return l1, l2


def solve_part1(s: str) -> int:
    """
    Solve AoC D1 P1.
    """
    l1, l2 = _parse_two_list(s)
    l1.sort()
    l2.sort()

    total = 0
    for n1, n2 in zip(l1, l2):
        total += abs(n1 - n2)

    return total


def solve_part2(s: str) -> int:
    """
    Solve AoC D1 P2.
    """
    l1, l2 = _parse_two_list(s)
    counter1, counter2 = Counter(l1), Counter(l2)

    total = 0
    for n, count in counter1.items():
        total += n * count * counter2[n]

    return total
