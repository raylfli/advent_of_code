"""
Advent of Code - Day 20: Race Condition
"""

from collections import defaultdict
import heapq
from itertools import product

type GridIndex = tuple[int, int]


def _parse_input(s: str) -> tuple[set[GridIndex], GridIndex, GridIndex]:
    """
    Parse input into list of walls, the start location and the end location.
    """
    walls: set[GridIndex] = set()
    start: GridIndex = (-1, -1)
    end: GridIndex = (-1, -1)
    for r, row in enumerate(s.strip().split("\n")):
        for c, cell in enumerate(row.strip()):
            if cell == "#":
                walls.add((r, c))
            elif cell == "S":
                start = (r, c)
            elif cell == "E":
                end = (r, c)
    return walls, start, end


def _retrace_path(
    parents: dict[GridIndex, GridIndex], end: GridIndex
) -> list[GridIndex]:
    """
    Retrace optimal path.
    """
    path = []
    prev = None
    curr = end
    while prev != curr:
        path.append(curr)
        prev = curr
        curr = parents[curr]
    return list(reversed(path))


def _a_star(
    obstacles: set[GridIndex], start: GridIndex, end: GridIndex
) -> list[GridIndex] | None:
    """
    Run A-Star from the start to end node returning the path.

    Returns None if no path is found.
    """
    frontier: list[(int, GridIndex)] = [(0, start)]
    costs: dict[GridIndex, int] = dict()
    parents: dict[GridIndex, GridIndex] = dict()
    costs[start] = 0
    parents[start] = start
    while len(frontier) > 0:
        _, p0 = heapq.heappop(frontier)
        cost0 = costs[p0]
        if p0 == end:
            return _retrace_path(parents, end)

        x0, y0 = p0
        for dx, dy in {(-1, 0), (1, 0), (0, -1), (0, 1)}:
            x1, y1 = x0 + dx, y0 + dy
            p1 = x1, y1
            # no OOB checking since grid is guaranteed to have walls around
            if p1 not in obstacles and p1 != parents[p0]:
                cost1 = cost0 + 1
                if p1 not in costs or cost1 < costs[p1]:
                    heapq.heappush(
                        frontier, (cost1 + abs(end[0] - x1) + abs(end[1] - y1), p1)
                    )
                    costs[p1] = cost1
                    parents[p1] = p0

    return None


def solve_part1(s: str, time_save: int = 100, cheat_time: int = 2) -> int:
    """
    Solve AoC D20 P1.
    """
    walls, start, end = _parse_input(s)

    # find unique path
    path = _a_star(walls, start, end)
    path_indices = {p: i for i, p in enumerate(path)}

    # then from each node, see if can jump to another part of the path
    cheat_neighbours = {
        (dr, dc)
        for dr, dc in product(range(-cheat_time, cheat_time + 1), repeat=2)
        if 1 < abs(dr) + abs(dc) <= cheat_time
    }

    shortcuts = defaultdict(lambda: 0)
    seen_cheats: set[tuple[GridIndex, GridIndex]] = set()
    for p0 in path:
        r0, c0 = p0
        for dr, dc in cheat_neighbours:
            r1, c1 = r0 + dr, c0 + dc
            p1 = r1, c1
            if p1 in path_indices and (p0, p1) not in seen_cheats:
                seen_cheats.add((p0, p1))
                saved = path_indices[p1] - path_indices[p0] - abs(dr) - abs(dc)
                shortcuts[saved] += 1

    return sum(count for saved, count in shortcuts.items() if saved >= time_save)


def solve_part2(s: str, time_save: int = 100) -> int:
    """
    Solve AoC D20 P2.
    """
    return solve_part1(s, time_save=time_save, cheat_time=20)
