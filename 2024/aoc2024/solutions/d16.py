"""
Advent of Code - Day 16: Reindeer Maze
"""

from collections import defaultdict
import heapq

type Grid = list[str]
type GridIndex = tuple[int, int]
type Direction = tuple[int, int]
type CostNode = tuple[int, GridIndex, Direction]


def _parse_grid(s: str) -> tuple[Grid, GridIndex, GridIndex]:
    """
    Parse the grid into a list[str] representation and find the reindeer start and end tiles.
    """
    grid = []
    start_loc = (-1, -1)
    end_loc = (-1, -1)
    for r, row in enumerate(s.strip().split("\n")):
        grid.append(row.strip())
        for c, cell in enumerate(row.strip()):
            if cell == "S":
                start_loc = (r, c)
            elif cell == "E":
                end_loc = (r, c)

    return grid, start_loc, end_loc


def _update_heap(
    heap: list[CostNode], update_loc: GridIndex, update_dir: Direction, new_cost: int
):
    """
    Update a heap's item with a new cost.
    """
    for i, (_, loc, d) in enumerate(heap):
        if loc == update_loc and d == update_dir:
            heap[i] = (new_cost, loc, d)
            heapq.heapify(heap)
            return

    raise ValueError("Could not find heap item.")


def _dijkstra_search(grid, start_loc, start_dir, end_loc) -> tuple[
    dict[tuple[GridIndex, Direction], int],
    dict[tuple[GridIndex, Direction], set[tuple[GridIndex, Direction]]],
]:
    """
    Perform Dijkstra's search on the grid.
    """
    possible_dirs = {(-1, 0), (1, 0), (0, -1), (0, 1)}

    dists: dict[tuple[GridIndex, Direction], int] = {(start_loc, start_dir): 0}
    prevs: dict[tuple[GridIndex, Direction], set[tuple[GridIndex, Direction]]] = (
        defaultdict(set)
    )
    prevs[(start_loc, start_dir)].add((start_loc, start_dir))

    heap: list[CostNode] = []
    heapq.heappush(heap, (0, start_loc, start_dir))
    while len(heap) > 0:

        _, l0, d0 = heapq.heappop(heap)
        node0 = l0, d0
        r0, c0 = l0

        for d1 in possible_dirs:
            dr1, dc1 = d1
            r1, c1 = r0 + dr1, c0 + dc1
            l1 = r1, c1
            if grid[r1][c1] != "#":
                if d0 == d1:
                    # move forward
                    cost1 = dists[node0] + 1
                    node1 = l1, d0
                else:
                    # turn
                    cost1 = dists[node0] + 1000
                    node1 = l0, d1

                if node1 not in dists or cost1 <= dists[node1]:
                    if node1 not in dists or cost1 < dists[node1]:
                        prevs[node1] = set()
                    dists[node1] = cost1
                    prevs[node1].add(node0)
                    heapq.heappush(heap, (cost1, *node1))

    return dists, prevs


def solve_part1(s: str) -> int:
    """
    Solve AoC D16 P1.
    """
    grid, start_loc, end_loc = _parse_grid(s)
    start_dir = (0, 1)  # start facing East

    dists, _ = _dijkstra_search(grid, start_loc, start_dir, end_loc)
    return min(
        dists.get((end_loc, d), float("inf"))
        for d in {(-1, 0), (1, 0), (0, -1), (0, 1)}
    )


def solve_part2(s: str) -> int:
    """
    Solve AoC D16 P2.
    """
    grid, start_loc, end_loc = _parse_grid(s)
    start_dir = (0, 1)  # start facing East

    dists, prevs = _dijkstra_search(grid, start_loc, start_dir, end_loc)
    to_check: list[tuple[GridIndex, Direction]] = []
    min_cost = min(
        dists.get((end_loc, d), float("inf"))
        for d in {(-1, 0), (1, 0), (0, -1), (0, 1)}
    )
    for d in {(-1, 0), (1, 0), (0, -1), (0, 1)}:
        if (end_loc, d) in prevs and dists[(end_loc, d)] == min_cost:
            to_check.extend(prevs[(end_loc, d)])

    part_of_best_path = {end_loc}
    while len(to_check) > 0:
        check_node = to_check.pop()
        loc, _ = check_node
        part_of_best_path.add(loc)
        if loc != start_loc:
            to_check.extend(prevs[check_node])
    return len(part_of_best_path)
