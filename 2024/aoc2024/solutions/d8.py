"""
Advent of Code - Day 8: Resonant Collinearity
"""

from collections import defaultdict
from itertools import combinations
from functools import reduce


def _get_antenna_locations(s: str) -> tuple[dict[str, set[tuple[int, int]]], int, int]:
    """
    Find the locations of all unique antennas.
    """
    locations = defaultdict(set)
    max_x = -1
    rows = s.strip().split('\n')
    max_y = len(rows) - 1
    for r, row in enumerate(rows):
        row = row.strip()
        max_x = len(row) - 1
        for c, cell in enumerate(row):
            if cell != '.':
                locations[cell].add((c, r))
    return locations, max_x, max_y


def compute_antinodes(antennas: set[tuple[int, int]],
                      max_x: int, max_y: int) -> set[tuple[int, int]]:
    """
    Compute the antinodes of these antennas.
    """
    antinodes = set()
    for (x1, y1), (x2, y2) in combinations(antennas, 2):
        dx, dy = x2 - x1, y2 - y1
        an1 = (x1 - dx, y1 - dy)
        an2 = (x2 + dx, y2 + dy)
        if 0 <= an1[0] <= max_x and 0 <= an1[1] <= max_y:
            antinodes.add(an1)
        if 0 <= an2[0] <= max_x and 0 <= an2[1] <= max_y:
            antinodes.add(an2)
    return antinodes


def compute_antinodes_infinite(antennas: set[tuple[int, int]],
                               max_x: int, max_y: int) -> set[tuple[int, int]]:
    """
    Compute the antinodes of these antennas as long as the antinodes are
    still within the maximum bounds.
    """
    antinodes = set()
    for (x1, y1), (x2, y2) in combinations(antennas, 2):
        dx = x2 - x1
        dy = y2 - y1

        # calculate a2 -> a1 direction antinodes
        an = (x1 + dx, y1 + dy)
        while True:
            an = (an[0] - dx, an[1] - dy)
            if 0 <= an[0] <= max_x and 0 <= an[1] <= max_y:
                antinodes.add(an)
            else:
                break

        # calculate a1 -> a2 direction antinodes
        an = (x2 - dx, y2 - dy)
        while True:
            an = (an[0] + dx, an[1] + dy)
            if 0 <= an[0] <= max_x and 0 <= an[1] <= max_y:
                antinodes.add(an)
            else:
                break

    return antinodes


def solve_part1(s: str, antinode_strategy: callable = compute_antinodes) -> int:
    """
    Solve AoC D8 P1.
    """
    antennas, max_x, max_y = _get_antenna_locations(s)
    antinodes = reduce(lambda acc, update: acc.union(antinode_strategy(update, max_x, max_y)),
                       antennas.values(),
                       set())
    return len(antinodes)


def solve_part2(s: str) -> int:
    """
    Solve AoC D8 P2.
    """
    return solve_part1(s, compute_antinodes_infinite)
