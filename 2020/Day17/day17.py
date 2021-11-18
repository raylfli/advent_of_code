""" ADVENT OF CODE 2020 - DAY 17 - RAYMOND LI """

from __future__ import annotations

import logging
from typing import Dict, List, Tuple


def read_input(filepath: str) -> List[List[str]]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        initial_state = input_file.read().strip().split('\n')

    return [list(r) for r in initial_state]


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 17 Part 1 problem.

    >>> solve_part1('test1.txt')
    112
    """
    logging.debug(f'EXECUTING SOLVE - 1')
    grid = read_input(filepath)

    shift = (1 - len(grid)) // 2
    space = {(x + shift, y + shift, 0): 1 if grid[x][y] == '#' else 0
             for x in range(len(grid))
             for y in range(len(grid[x]))
             }

    for _ in range(6):
        space = do_cycle(space)

    return sum(space.values())


def do_cycle(space: Dict[Tuple[int, int, int], int]) -> Dict[Tuple[int, int, int], int]:
    """Return the new space after one cycle.
    """
    new_space = dict()
    make_space(space)
    for coord, value in space.items():
        active = 0
        for neighbour in get_neighbours(*coord):
            if space.get(neighbour, 0) == 1:
                active += 1

        if value == 1:
            new_space[coord] = 1 if active == 2 or active == 3 else 0
        elif value == 0:
            new_space[coord] = 1 if active == 3 else 0
        else:
            logging.warning(f'Something went wrong...')

    return new_space


def make_space(space: Dict[Tuple[int, int, int], int]) -> None:
    """Mutate the given space to give it more space.
    """
    xs, ys, zs = zip(*space)
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    z_min, z_max = min(zs), max(zs)
    for x in range(x_min - 1, x_max + 2):
        for y in range(y_min - 1, y_max + 2):
            for z in range(z_min - 1, z_max + 2):
                coord = (x, y, z)
                if coord not in space:
                    space[coord] = 0


def get_neighbours(x: int, y: int, z: int) -> List[Tuple[int, int, int]]:
    """Return a list of neighbours of the given x, y, z.
    """
    return [(a, b, c)
            for a in range(x - 1, x + 2)
            for b in range(y - 1, y + 2)
            for c in range(z - 1, z + 2)
            if a != x or b != y or c != z
            ]


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 17 Part 2 problem.

    >>> solve_part2('test1.txt')
    848
    """
    logging.debug(f'EXECUTING SOLVE - 2')
    grid = read_input(filepath)

    shift = (1 - len(grid)) // 2
    space = {(x + shift, y + shift, 0, 0): 1 if grid[x][y] == '#' else 0
             for x in range(len(grid))
             for y in range(len(grid[x]))
             }

    for _ in range(6):
        space = do_cycle_4d(space)

    return sum(space.values())


def do_cycle_4d(space: Dict[Tuple[int, int, int, int], int]) -> Dict[Tuple[int, int, int, int], int]:
    """Return the new space after one cycle.

    This function operates in 4-D.
    """
    new_space = dict()
    make_space_4d(space)
    for coord, value in space.items():
        active = 0
        for neighbour in get_neighbours_4d(*coord):
            if space.get(neighbour, 0) == 1:
                active += 1

        if value == 1:
            new_space[coord] = 1 if active == 2 or active == 3 else 0
        elif value == 0:
            new_space[coord] = 1 if active == 3 else 0
        else:
            logging.warning(f'Something went wrong...')

    return new_space


def make_space_4d(space: Dict[Tuple[int, int, int, int], int]) -> None:
    """Mutate the given space to give it more space.
    """
    xs, ys, zs, ws = zip(*space)
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    z_min, z_max = min(zs), max(zs)
    w_min, w_max = min(ws), max(ws)
    for x in range(x_min - 1, x_max + 2):
        for y in range(y_min - 1, y_max + 2):
            for z in range(z_min - 1, z_max + 2):
                for w in range(w_min - 1, w_max + 2):
                    coord = (x, y, z, w)
                    if coord not in space:
                        space[coord] = 0


def get_neighbours_4d(x: int, y: int, z: int, w: int) -> List[Tuple[int, int, int, int]]:
    """Return a list of neighbours of the given x, y, z.
    """
    return [(a, b, c, d)
            for a in range(x - 1, x + 2)
            for b in range(y - 1, y + 2)
            for c in range(z - 1, z + 2)
            for d in range(w - 1, w + 2)
            if a != x or b != y or c != z or d != w
            ]


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D17P1: {solve_part1("input.txt")}')
    print(f'D17P2: {solve_part2("input.txt")}')
