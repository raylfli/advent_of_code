"""
Advent of Code - Day 13: Claw Contraption
"""

import re

type ButtonIncrement = tuple[int, int]
type GridIndex = tuple[int, int]

PATT_COORDINATE = re.compile(r"X[+=](\d+), Y[+=](\d+)")


def _parse_setup(
    s: str, prize_incr: int = 0
) -> tuple[ButtonIncrement, ButtonIncrement, GridIndex]:
    """
    Parse single claw machine setup.
    """
    matches = re.findall(PATT_COORDINATE, s)

    assert len(matches) == 3
    return (
        (int(matches[0][0]), int(matches[0][1])),
        (int(matches[1][0]), int(matches[1][1])),
        (prize_incr + int(matches[2][0]), prize_incr + int(matches[2][1])),
    )


def _parse_setups(
    s: str, prize_incr: int = 0
) -> list[tuple[ButtonIncrement, ButtonIncrement, GridIndex]]:
    """
    Parse claw machine setups.
    """
    machines = s.strip().split("\n\n")
    return [_parse_setup(machine, prize_incr=prize_incr) for machine in machines]


def _collect_prize(
    machine: tuple[ButtonIncrement, ButtonIncrement, GridIndex],
    max_presses: float = 100,
) -> int:
    """
    Find the minimum number of tokens to collect the prize. Return -1 if prize cannot be reached.
    """
    (ax, ay), (bx, by), (px, py) = machine

    b = (ax * py - ay * px) / (ax * by - ay * bx)
    a = (px - b * bx) / ax

    if (
        a.is_integer()
        and b.is_integer()
        and 0 <= a <= max_presses
        and 0 <= b <= max_presses
    ):
        return int(a * 3 + b)
    else:
        return -1


def solve_part1(s: str) -> int:
    """
    Solve AoC D13 P1.
    """
    machines = _parse_setups(s)
    total = 0
    for machine in machines:
        tokens = _collect_prize(machine)
        if tokens >= 0:
            total += tokens
    return total


def solve_part2(s: str) -> int:
    """
    Solve AoC D13 P2.
    """
    machines = _parse_setups(s, prize_incr=10000000000000)
    total = 0
    for machine in machines:
        tokens = _collect_prize(machine, max_presses=float("inf"))
        if tokens >= 0:
            total += tokens
    return total
