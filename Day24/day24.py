""" ADVENT OF CODE 2020 - DAY 24 - RAYMOND LI """

from __future__ import annotations

import logging
from typing import Dict, Tuple

HEXAGONAL_SURROUNDINGS = {(1, 0), (-1, 0), (0.5, 1), (-0.5, 1), (0.5, -1), (-0.5, -1)}


def read_input(filepath: str) -> Dict[Tuple[int, int], int]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        instructions = input_file.read().strip().split('\n')

    tiles = {}  # Dict[Tuple[int, int], int]
    for instruction in instructions:
        coord = parse_tile_location(instruction)
        if coord not in tiles:
            tiles[coord] = 1
        else:
            tiles[coord] *= -1

    return tiles


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 24 Part 1 problem.

    >>> solve_part1('test1.txt')
    10
    """
    logging.debug(f'EXECUTING SOLVE - 1')
    tiles = read_input(filepath)

    return len([tile for tile in tiles if tiles[tile] == 1])


def parse_tile_location(tile: str) -> Tuple[float, float]:
    """Parses the given tile's location as identified by location away from the reference point,
    in this case (0, 0).

    >>> parse_tile_location('esenee')
    (3.0, 0.0)
    >>> parse_tile_location('esew')
    (0.5, -1.0)
    >>> parse_tile_location('nwwswee')
    (0.0, 0.0)
    """
    x, y = 0.0, 0.0
    i = 0
    while i < len(tile):
        if tile[i] in {'n', 's'}:
            if tile[i] == 'n':
                y += 1
            elif tile[i] == 's':
                y -= 1

            if tile[i + 1] == 'e':
                x += 0.5
            elif tile[i + 1] == 'w':
                x -= 0.5

            i += 2

        elif tile[i] in {'e', 'w'}:
            if tile[i] == 'e':
                x += 1
            elif tile[i] == 'w':
                x -= 1

            i += 1

    return (x, y)


def solve_part2(filepath: str, days: int) -> int:
    """Returns solution to Day 24 Part 2 problem.

    >>> solve_part2('test1.txt', 100)
    2208
    >>> solve_part2('test1.txt', 60)
    788
    >>> solve_part2('test1.txt', 10)
    37
    >>> solve_part2('test1.txt', 3)
    25
    >>> solve_part2('test1.txt', 1)
    15
    """
    logging.debug(f'EXECUTING SOLVE - 2')
    tiles = read_input(filepath)

    for _ in range(days):
        add_surroundings(tiles)
        simulate_day(tiles)

    return len([tile for tile in tiles if tiles[tile] == 1])


def add_surroundings(tiles: Dict[Tuple[float, float], int]) -> None:
    """Add new tiles into the tiles dictionary.

    This function adds the 6 tiles surrounding each tile currently in the dictionary if needed.
    """
    tile_keys = set(tiles.keys())
    for tile in tile_keys:
        for surrounding in HEXAGONAL_SURROUNDINGS:
            test_coord = (tile[0] + surrounding[0], tile[1] + surrounding[1])
            if test_coord not in tiles:
                tiles[test_coord] = -1


def simulate_day(tiles: Dict[Tuple[float, float], int]) -> None:
    """Simulates one day in the resort lobby.
    """
    held_tiles = tiles.copy()
    for tile in tiles:
        adjacent_black = num_adjacent_black(held_tiles, tile)
        if tiles[tile] == 1:
            if adjacent_black == 0 or adjacent_black > 2:
                tiles[tile] = -1
        elif tiles[tile] == -1:
            if adjacent_black == 2:
                tiles[tile] = 1


def num_adjacent_black(tiles: Dict[Tuple[float, float], int], coord: Tuple[float, float]) -> int:
    """Return the number of adjacent tiles that are black for the tile at the given coord.

    Coordinates should be in the form of (x, y).

    Tiles that have a value of 1 are considered black, with any other value being considered white.

    If a tile is not in the dictionary of tiles, it will be white by default.
    """
    count = 0
    for surrounding in HEXAGONAL_SURROUNDINGS:
        if tiles.get((coord[0] + surrounding[0], coord[1] + surrounding[1]), -1) == 1:
            count += 1

    return count


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D24P1: {solve_part1("input.txt")}')
    print(f'D24P2: {solve_part2("input.txt", 100)}')
