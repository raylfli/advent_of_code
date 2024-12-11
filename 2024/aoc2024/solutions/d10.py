"""
Advent of Code - Day 10: Hoof It
"""

from collections.abc import Callable


def _parse_grid(s: str) -> list[list[int]]:
    """
    Parse the grid into 2D array.
    """
    grid = []
    for row in s.strip().split('\n'):
        grid.append([])
        for cell in row.strip():
            grid[-1].append(int(cell))
    return grid


def _setup_metric_array[T](grid: list[list[int]], init_nine: Callable[[int, int], T],
                           init_blank: Callable[[], T]):
    """
    Return initialized metrics array.

    `init_nine` is a callable mapping a grid row and column to a representation
    if the topographic map indicates a 9.

    `init_blank` is a callable mapping any other grid cell.
    """
    scores = []
    for r, row in enumerate(grid):
        scores.append([])
        for c, cell in enumerate(row):
            scores[-1].append(init_nine(r, c) if cell == 9 else init_blank())
    return scores


def _update_metric[T](grid: list[list[int]], scores: list[list[T]], height: int,
                      strategy: Callable[[T, T], T]):
    """
    Update the metrics array.

    `strategy` is a callable combining the current value of the metric
     with the metric of a neighbour of height `height + 1`.
    """
    neighbours = {(-1, 0), (0, -1), (1, 0), (0, 1)}
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == height:
                for dr, dc in neighbours:
                    check_r, check_c = r + dr, c + dc
                    if 0 <= check_r < len(grid) and 0 <= check_c < len(grid[0]) and \
                            grid[check_r][check_c] == height + 1:
                        scores[r][c] = strategy(scores[r][c], scores[check_r][check_c])


def _compute_trailhead_metric[T](grid: list[list[int]], scores: list[list[T]],
                                 strategy: Callable[[T], int]):
    """
    Compute the trailhead metric.

    `strategy` is a callable mapping a metric representation to an integer metric value.
    """
    total = 0
    for r, row in enumerate(scores):
        for c, cell in enumerate(row):
            if grid[r][c] == 0:
                total += strategy(cell)
    return total


def solve_part1(s: str) -> int:
    """
    Solve AoC D10 P1.
    """
    grid = _parse_grid(s)
    scores = _setup_metric_array(grid, lambda r, c: {(r, c)}, set)

    # update score
    for height in range(8, -1, -1):
        _update_metric(grid, scores, height,
                       strategy=lambda old_score, new_score: old_score.union(new_score))

    return _compute_trailhead_metric(grid, scores, len)


def solve_part2(s: str) -> int:
    """
    Solve AoC D10 P2.
    """
    grid = _parse_grid(s)
    scores = _setup_metric_array(grid, lambda _r, _c: 1, lambda: 0)

    for height in range(8, -1, -1):
        _update_metric(grid, scores, height,
                       strategy=lambda old_score, new_score: old_score + new_score)

    return _compute_trailhead_metric(grid, scores, lambda cell: cell)
