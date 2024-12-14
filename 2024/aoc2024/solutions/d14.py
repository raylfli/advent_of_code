"""
Advent of Code - Day 14: Restroom Redoubt
"""

from functools import reduce
import re

# (x, y, dx, dy)
type Robot = tuple[int, int, int, int]

PATT_ROBOT = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')


def _parse_robot(s: str) -> Robot:
    """
    Parse a single robot's position and velocity.
    """
    match = re.match(PATT_ROBOT, s.strip())
    return (
        int(match[1]), int(match[2]),
        int(match[3]), int(match[4])
    )


def _parse_robots(s: str) -> list[Robot]:
    """
    Parse the input string into a list of robot positions and velocity.
    """
    return [_parse_robot(line) for line in s.strip().split('\n')]


def _simulate_movement(robots: list[Robot], space_size: tuple[int, int] = (101, 103),
                       seconds: int = 100) -> list[Robot]:
    """
    Simulate movement of the robots for a number of seconds.
    """
    max_x, max_y = space_size
    new_robots = []
    for x0, y0, dx, dy in robots:
        x1 = (x0 + seconds * dx) % max_x
        y1 = (y0 + seconds * dy) % max_y
        new_robots.append((x1, y1, dx, dy))
    return new_robots


def _simulate_movement_step(robots: list[Robot], space_size: tuple[int, int] = (101, 103)):
    """
    Simulate movement of the robots for one second. Mutates the robots input list.
    """
    max_x, max_y = space_size
    for i, (x0, y0, dx, dy) in enumerate(robots):
        x1 = (x0 + dx) % max_x
        y1 = (y0 + dy) % max_y
        robots[i] = (x1, y1, dx, dy)


def _quadrant_count(robots: list[Robot], space_size: tuple[int, int]) -> tuple[int, int, int, int]:
    """
    Count the number of robots in each quadrant.

    Robots on the quadrant boundaries are not counted.
    """
    max_x, max_y = space_size
    mid_x, mid_y = max_x // 2, max_y // 2

    # quadrants:
    # 1 2
    # 3 4
    quad_1 = quad_2 = quad_3 = quad_4 = 0
    for x, y, _dx, _dy in robots:
        if 0 <= x < mid_x:
            if 0 <= y < mid_y:
                quad_1 += 1
            elif mid_y < y < max_y:
                quad_3 += 1
        elif mid_x < x < max_x:
            if 0 <= y < mid_y:
                quad_2 += 1
            elif mid_y < y < max_y:
                quad_4 += 1
    return (quad_1, quad_2, quad_3, quad_4)


def _str_robots(robots: list[Robot], space_size: tuple[int, int]):
    """
    Generate a picture of the robots.
    """
    locations = set((x, y) for x, y, _dx, _dy in robots)
    grid = []
    for r in range(0, space_size[0]):
        grid.append([])
        for c in range(0, space_size[1]):
            if (c, r) in locations:
                grid[-1].append('#')
            else:
                grid[-1].append('.')

    str_grid = []
    for row in grid:
        str_grid.append(''.join(row))
    return '\n'.join(str_grid)


def solve_part1(s: str, space_size: tuple[int, int] = (101, 103)) -> int:
    """
    Solve AoC D14 P1.
    """
    robots0 = _parse_robots(s)
    robots1 = _simulate_movement(robots0, space_size=space_size)
    return reduce(lambda acc, upd: acc * upd, _quadrant_count(robots1, space_size=space_size), 1)


def solve_part2(s: str, space_size: tuple[int, int] = (101, 103)) -> int:
    """
    Solve AoC D14 P2.

    This solution may not be consistent... It is a heuristic assuming most of the robots
    will be in one quadrant.

    The solution would fail if the robots form a Christmas tree around the centre.
    """
    robots0 = _parse_robots(s)
    robots = _parse_robots(s)
    counts = [reduce(lambda acc, upd: acc * upd, _quadrant_count(robots, space_size=space_size), 1)]
    for _ in range(0, 10000):
        _simulate_movement_step(robots, space_size=space_size)
        counts.append(
            reduce(lambda acc, upd: acc * upd, _quadrant_count(robots, space_size=space_size), 1))

    # find best match to a Christmas tree
    min_i = 0
    for i, count in enumerate(counts):
        if count < counts[min_i]:
            min_i = i
    robot_s = _str_robots(_simulate_movement(robots0, space_size=space_size, seconds=min_i),
                          space_size=space_size)
    print(robot_s)

    return min_i
