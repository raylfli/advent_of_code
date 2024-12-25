"""
Advent of Code - Day 25: Code Chronicle
"""

type PinHeights = list[int]
type KeyHeights = list[int]


def _parse_pin_or_key(s: str) -> tuple[bool, PinHeights | KeyHeights]:
    """
    Parse lock/key representation into heights.

    Return whether it is a lock and the corresponding height.
    """
    lines = s.strip().split("\n")
    if s[0] == "#":
        # we have a lock
        cols: list[int] = [0] * 5
        for line in lines[1:]:
            for i, c in enumerate(line.strip()):
                if c == "#":
                    cols[i] += 1
        return True, cols
    else:
        # we have a key
        cols = [0] * 5
        for line in lines[:-1]:
            for i, c in enumerate(line.strip()):
                if c == "#":
                    cols[i] += 1
        return False, cols


def _parse_input(s: str) -> tuple[list[PinHeights], list[KeyHeights]]:
    """
    Parse the input into pin and key heights.
    """
    lock_or_key = s.strip().split("\n\n")
    locks = []
    keys = []
    for lk in lock_or_key:
        is_lock, heights = _parse_pin_or_key(lk)
        if is_lock:
            locks.append(heights)
        else:
            keys.append(heights)
    return locks, keys


def solve_part1(s: str) -> int:
    """
    Solve AoC D25 P1.
    """
    locks, keys = _parse_input(s)

    pairs = set()
    for i, key in enumerate(keys):
        for j, lock in enumerate(locks):
            if all(lh + kh <= 5 for kh, lh in zip(key, lock)):
                pairs.add((i, j))

    return len(pairs)


def solve_part2(_s: str) -> int:
    """
    Solve AoC D25 P2.

    Day 25 has no part 2. It is always a star gate!
    """
    return 0
