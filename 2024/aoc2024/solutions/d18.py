"""
Advent of Code - Day 18: RAM Run
"""

import heapq

type GridIndex = tuple[int, int]


def _parse_input(s: str, num_locations: int = -1) -> set[GridIndex]:
    """
    Parse input into a corruption locations.

    If `num_locations == -1`, returns all locations. Otherwise returns
    only `num_locations` many.
    """
    locs = set()
    for line in s.strip().split("\n"):
        if num_locations != -1 and len(locs) == num_locations:
            return locs

        x, y = line.strip().split(",", maxsplit=1)
        locs.add((int(x), int(y)))

    return locs


def _parse_input_lst(s: str) -> list[GridIndex]:
    """
    Parse input into a corruption locations.
    """
    locs = []
    for line in s.strip().split("\n"):
        x, y = line.strip().split(",", maxsplit=1)
        locs.append((int(x), int(y)))
    return locs


def _a_star(corrupted: set[GridIndex], mem_size: int) -> int:
    """
    Run A-Star from cell (0, 0) to (mem_size, mem_size).

    Returns -1 if no path is found.
    """
    frontier: list[(int, GridIndex)] = [(0, (0, 0))]
    costs: dict[GridIndex, int] = dict()
    parents: dict[GridIndex, GridIndex] = dict()
    costs[(0, 0)] = 0
    parents[(0, 0)] = (0, 0)
    while len(frontier) > 0:
        _, p0 = heapq.heappop(frontier)
        cost0 = costs[p0]
        if p0 == (mem_size, mem_size):
            return costs[p0]

        x0, y0 = p0
        for dx, dy in {(-1, 0), (1, 0), (0, -1), (0, 1)}:
            x1, y1 = x0 + dx, y0 + dy
            p1 = x1, y1
            if (
                0 <= x1 <= mem_size
                and 0 <= y1 <= mem_size
                and p1 not in corrupted
                and p1 != parents[p0]
            ):
                cost1 = cost0 + 1
                if p1 not in costs or cost1 < costs[p1]:
                    heapq.heappush(
                        frontier, (cost1 + abs(mem_size - x1) + abs(mem_size - y1), p1)
                    )
                    costs[p1] = cost1
                    parents[p1] = p0

    return -1


def solve_part1(s: str, mem_size: int = 70, num_locations: int = 1024) -> int:
    """
    Solve AoC D18 P1.
    """
    corrupted = _parse_input(s, num_locations=num_locations)

    return _a_star(corrupted, mem_size=mem_size)


def solve_part2(s: str, mem_size: int = 70) -> tuple[int, int] | None:
    """
    Solve AoC D18 P2.
    """
    all_corr = _parse_input_lst(s)
    for i, cell in enumerate(all_corr):
        corr = _parse_input(s, num_locations=i + 1)
        if _a_star(corr, mem_size=mem_size) == -1:
            return cell
    return None
