"""
Advent of Code - Day 21: Keypad Conundrum
"""

from collections import deque
from functools import cache
from itertools import pairwise


NUMPAD = {
    "A": [("0", "<"), ("3", "^")],
    "0": [("2", "^"), ("A", ">")],
    "1": [("2", ">"), ("4", "^")],
    "2": [("0", "v"), ("1", "<"), ("3", ">"), ("5", "^")],
    "3": [("2", "<"), ("6", "^"), ("A", "v")],
    "4": [("1", "v"), ("5", ">"), ("7", "^")],
    "5": [("2", "v"), ("4", "<"), ("6", ">"), ("8", "^")],
    "6": [("3", "v"), ("5", "<"), ("9", "^")],
    "7": [("4", "v"), ("8", ">")],
    "8": [("5", "v"), ("7", "<"), ("9", ">")],
    "9": [("6", "v"), ("8", "<")],
}

DPAD = {
    "A": [("^", "<"), (">", "v")],
    "^": [("A", ">"), ("v", "v")],
    "<": [("v", ">")],
    "v": [("<", "<"), ("^", "^"), (">", ">")],
    ">": [("v", "<"), ("A", "^")],
}


@cache
def _find_paths(numpad: bool, start: str, end: str) -> list[str]:
    """
    Find all the shortest paths between `start` and `end`.
    """
    if numpad:
        neighbours = NUMPAD
    else:
        neighbours = DPAD

    frontier: deque[tuple[str, list[str]]] = deque([(start, [])])
    explored: set[str] = {start}
    best_paths: list[str] = []
    while len(frontier) > 0:
        curr, path = frontier.popleft()
        if curr == end and (
            len(best_paths) == 0 or len(path) + 1 == len(best_paths[0])
        ):
            best_paths.append("".join(path) + "A")
            continue
        if len(best_paths) > 0 and len(path) >= len(best_paths[0]):
            continue
        for label, direc in neighbours[curr]:
            explored.add(label)
            frontier.append((label, path + [direc]))
    return best_paths


@cache
def _find_least_keystrokes_recur(
    code: str, robots: int = 2, numpad: bool = True
) -> int:
    """
    Find the least amount of button presses on the main dpad to enter a sequence on the numpad.
    """
    code = "A" + code  # all robots start by pointing at A
    min_keystrokes = 0
    for a, b in pairwise(code):
        # find paths between required buttons
        paths = _find_paths(numpad, a, b)
        if robots == 0:
            # this robot has a human controlling it (can just press buttons)
            min_keystrokes += min(map(len, paths))
        else:
            # this robot has another robot controlling it (need to move the arm to hit buttons)
            min_keystrokes += min(
                _find_least_keystrokes_recur(path, robots=robots - 1, numpad=False)
                for path in paths
            )
    return min_keystrokes


def _find_least_keystrokes(code: str, robots: int = 2) -> int:
    """
    Find the least amount of button presses on the main dpad to enter a sequence on the numpad.
    """
    return _find_least_keystrokes_recur(code, robots=robots)


def solve_part1(s: str, robots: int = 2) -> int:
    """
    Solve AoC D21 P1.
    """
    codes = [line.strip() for line in s.strip().split("\n")]

    total = 0
    for code in codes:
        n = int(code[:-1])
        least = _find_least_keystrokes(code, robots=robots)
        total += n * least
    return total


def solve_part2(s: str) -> int:
    """
    Solve AoC D21 P2.
    """
    return solve_part1(s, robots=25)
