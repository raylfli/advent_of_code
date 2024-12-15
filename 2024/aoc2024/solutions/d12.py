"""
Advent of Code - Day 12: Garden Groups
"""

from collections import defaultdict
from itertools import pairwise

type GridIndex = tuple[int, int]
type RegionId = tuple[str, int]


def _parse_grid(s: str) -> list[str]:
    """
    Parse the grid into a list representation.
    """
    grid = []
    for row in s.strip().split("\n"):
        grid.append(row.strip())
    return grid


def _matching_neighbours(grid: list[str], r: int, c: int) -> set[GridIndex]:
    """
    Return the locations of matching neighbours beside (r, c) on the 4-connected grid.
    """
    neighbours = {(-1, 0), (0, -1), (1, 0), (0, 1)}
    matching = set()  # set[GridIndex]
    for dr, dc in neighbours:
        check_r, check_c = r + dr, c + dc
        if 0 <= check_r < len(grid) and 0 <= check_c < len(grid[0]):
            if grid[r][c] == grid[check_r][check_c]:
                matching.add((check_r, check_c))
    return matching


def _open_neighbours(grid: list[str], r: int, c: int) -> set[GridIndex]:
    """
    Return the directions of non-matching neighbours beside (r, c) on the 4-connected grid.
    """
    neighbours = {(-1, 0), (0, -1), (1, 0), (0, 1)}
    non_matching = set()  # set[GridIndex]
    for dr, dc in neighbours:
        check_r, check_c = r + dr, c + dc
        if 0 <= check_r < len(grid) and 0 <= check_c < len(grid[0]):
            if grid[r][c] != grid[check_r][check_c]:
                non_matching.add((dr, dc))
        else:
            non_matching.add((dr, dc))
    return non_matching


def _process_region(
    grid: list[str],
    region_map: dict[GridIndex, RegionId],
    areas: dict[RegionId, int],
    perimeters: dict[RegionId, int],
    plant_region_count: dict[str, int],
    r: int,
    c: int,
    perimeter_cells: dict[RegionId, set[GridIndex]] = None,
):
    """
    Process an entire region since we've found a new region.
    """
    # set up region ID
    cell = grid[r][c]
    region_id = cell, plant_region_count[cell]
    plant_region_count[cell] += 1

    # process all neighbours of this region
    visited = set()  # set[GridIndex]
    frontier = [(r, c)]  # list[GridIndex]
    while len(frontier) > 0:
        check_i = frontier.pop()
        if check_i in visited:
            continue
        visited.add(check_i)
        region_map[check_i] = region_id

        matching = _matching_neighbours(grid, *check_i)
        num_neighbours = len(matching)
        areas[region_id] += 1
        perimeters[region_id] += 4 - num_neighbours

        # track any perimeter cell
        if perimeter_cells is not None and num_neighbours != 4:
            perimeter_cells[region_id].add(check_i)

        frontier.extend(matching)


def _calculate_num_sides(grid: list[str], perimeter_cells: set[GridIndex]) -> int:
    """
    Walk the perimeter of a region and find the number of sides it has.

    INSPIRED BY https://www.reddit.com/r/adventofcode/comments/1hcxmpp/2024_day_12_part_2_visualisation_of_my_first/
    """
    # for each point
    # - find which 'open' boundaries it has (i.e. which directions have fences)
    # - add the point to a set of those directional fences
    fence_sides = defaultdict(list)
    for r, c in perimeter_cells:
        open_neighbours = _open_neighbours(grid, r, c)
        for on in open_neighbours:
            fence_sides[on].append((r, c))

    # then for each direction
    # - find consecutive fence segments
    sides = 0
    for (dr, _), cells in fence_sides.items():
        # dr == 0 means left/right side fences
        # dc == 0 means top/bottom side fences
        fixed_i = 1 if dr == 0 else 0
        unfixed_i = 1 - fixed_i

        groups = defaultdict(list)  # dict[int, list[int]]
        for cell in cells:
            groups[cell[fixed_i]].append(cell[unfixed_i])

        for fence_cells in groups.values():
            if len(fence_cells) == 1:
                sides += 1
                continue

            fence_cells.sort()
            these_sides = 1
            for a, b in pairwise(fence_cells):
                if a + 1 != b:
                    these_sides += 1

            sides += these_sides

    return sides


def _calculate_fence_price(areas: dict[RegionId, int], perimeters: dict[RegionId, int]):
    """
    Calculate the price of fences.

    Assumptions:
    - areas.keys() == perimeters.keys()
    """
    price = 0
    for region_id, area in areas.items():
        price += area * perimeters[region_id]
    return price


def solve_part1(s: str) -> int:
    """
    Solve AoC D12 P1.
    """
    grid = _parse_grid(s)

    # multiple identical letter regions can show up, track how many
    plant_region_count = defaultdict(lambda: 0)  # dict[str, int]

    # index distinct regions with RegionId

    # track areas and perimeters of each plot
    areas = defaultdict(lambda: 0)  # dict[GridIndex, int]
    perimeters = defaultdict(lambda: 0)  # dict[RegionId, int]

    # map each cell back to a region ID
    region_map = dict()  # dict[GridIndex, RegionId]

    # map each cell to a region and track area/perimeter
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            # no need to process multiple times
            if (r, c) in region_map:
                continue

            _process_region(
                grid, region_map, areas, perimeters, plant_region_count, r, c
            )

    return _calculate_fence_price(areas, perimeters)


def solve_part2(s: str) -> int:
    """
    Solve AoC D12 P2.
    """
    grid = _parse_grid(s)

    # multiple identical letter regions can show up, track how many
    plant_region_count = defaultdict(lambda: 0)  # dict[str, int]

    # index distinct regions with RegionId

    # track areas and perimeters of each plot
    areas = defaultdict(lambda: 0)  # dict[GridIndex, int]
    perimeters = defaultdict(lambda: 0)  # dict[RegionId, int]
    perimeter_cells = defaultdict(set)  # dict[RegionId, set[GridIndex]]

    # map each cell back to a region ID
    region_map = dict()  # dict[GridIndex, RegionId]

    # map each cell to a region and track area/perimeter
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            # no need to process multiple times
            if (r, c) in region_map:
                continue

            _process_region(
                grid,
                region_map,
                areas,
                perimeters,
                plant_region_count,
                r,
                c,
                perimeter_cells,
            )

    # calculate sides
    num_sides = dict()  # dict[RegionId, int]
    for region_id, perim_cells in perimeter_cells.items():
        num_sides[region_id] = _calculate_num_sides(grid, perim_cells)

    return _calculate_fence_price(areas, num_sides)
