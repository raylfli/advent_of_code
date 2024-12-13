"""
Advent of Code - Day 12: Garden Groups
"""

from collections import defaultdict

type GridIndex = tuple[int, int]
type RegionId = tuple[str, int]


def _parse_grid(s: str) -> list[str]:
    """
    Parse the grid into a list representation.
    """
    grid = []
    for row in s.strip().split('\n'):
        grid.append(row.strip())
    return grid


def _matching_neighbours_4(grid: list[str], r: int, c: int) -> set[GridIndex]:
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


def _matching_neighbours_8(grid: list[str], r: int, c: int) -> set[GridIndex]:
    """
    Return the locations of matching neighbours beside (r, c) on the 8-connected grid.
    """
    neighbours = {(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)}
    matching = set()  # set[GridIndex]
    for dr, dc in neighbours:
        check_r, check_c = r + dr, c + dc
        if 0 <= check_r < len(grid) and 0 <= check_c < len(grid[0]):
            if grid[r][c] == grid[check_r][check_c]:
                matching.add((check_r, check_c))
    return matching


def _process_region(grid: list[str], region_map: dict[GridIndex, RegionId],
                    areas: dict[RegionId, int], perimeters: dict[RegionId, int],
                    plant_region_count: dict[str, int], r: int, c: int,
                    perimeter_cells: dict[RegionId, set[GridIndex]] = None):
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

        matching = _matching_neighbours_4(grid, *check_i)
        num_neighbours = len(matching)
        areas[region_id] += 1
        perimeters[region_id] += 4 - num_neighbours

        # track any perimeter cell
        if perimeter_cells is not None and num_neighbours != 4:
            perimeter_cells[region_id].add(check_i)

        frontier.extend(matching)


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

            _process_region(grid, region_map, areas, perimeters, plant_region_count, r, c)

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

            _process_region(grid, region_map, areas, perimeters, plant_region_count, r, c,
                            perimeter_cells)

    return _calculate_fence_price(areas, perimeters)
