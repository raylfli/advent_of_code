"""
Advent of Code - Day 11: Plutonian Pebbles
"""

from collections import defaultdict


def _blink_stone(marking: int) -> list[int]:
    """
    Blink a single stone based on the puzzle rules.
    """
    if marking == 0:
        return [1]
    s = str(marking)
    if len(s) % 2 == 0:
        return [int(s[: len(s) // 2]), int(s[len(s) // 2 :])]
    return [marking * 2024]


def solve_part1(s: str, blinks: int = 25) -> int:
    """
    Solve AoC D11 P1.
    """
    stones = [int(n) for n in s.strip().split(" ")]

    stone_map = defaultdict(
        lambda: 0
    )  # dict[int, int] marking -> number of occurrences
    for stone in stones:
        stone_map[stone] += 1

    for _ in range(blinks):
        new_stone_map = defaultdict(lambda: 0)
        for marking, count in stone_map.items():
            new_stones = _blink_stone(marking)
            for stone in new_stones:
                new_stone_map[stone] += count
        stone_map = new_stone_map

    return sum(v for v in stone_map.values())


def solve_part2(s: str) -> int:
    """
    Solve AoC D11 P2.
    """
    return solve_part1(s, 75)
