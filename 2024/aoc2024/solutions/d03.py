"""
Advent of Code - Day 3: Mull It Over
"""

import re


def _extract_mul(s: str) -> list[(int, int)]:
    """
    Extract all valid mul(a,b) instances.
    """
    matches = re.findall(r"mul\((\d+?),(\d+?)\)", s)
    return [(int(match[0]), int(match[1])) for match in matches]


def _instruction_generator(s: str) -> str:
    """
    Yields characters from the instruction if they are outside of don't()/do() blocks.
    """
    enable = True
    for i, c in enumerate(s):
        if s[i : i + 7] == "don't()":
            enable = False
        elif s[i : i + 4] == "do()":
            enable = True

        if enable:
            yield c


def solve_part1(s: str) -> int:
    """
    Solve AoC D3 P1.
    """
    return sum(a * b for a, b in _extract_mul(s))


def solve_part2(s: str) -> int:
    """
    Solve AoC D3 P2.
    """
    s = "".join(_instruction_generator(s))
    return solve_part1(s)
