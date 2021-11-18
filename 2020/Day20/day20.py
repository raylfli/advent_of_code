""" ADVENT OF CODE 2020 - DAY 20 - RAYMOND LI """

from __future__ import annotations

import logging
import math
import re
from typing import Dict, List, Optional, Set, Tuple, Union

RE_DIGITS = re.compile(r'\d+')
MONSTER = [[18], [0, 5, 6, 11, 12, 17, 18, 19], [1, 4, 7, 10, 13, 16]]


def read_input(filepath: str) -> Tuple[Dict[int, List[str]], int, Set[int]]:
    """Return processed version of the puzzle input.

    Returned tuple is in the format of: (tiles, side length of tiles, all tile ids)
    """
    with open(filepath) as input_file:
        tiles = input_file.read().strip().split('\n\n')

    tiles = [tile.split('\n') for tile in tiles]
    tiles = {int(re.search(RE_DIGITS, tile[0])[0]): tile[1:] for tile in tiles}
    side_length = int(math.sqrt(len(tiles)))
    all_ids = set(tiles)

    return (tiles, side_length, all_ids)


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 20 Part 1 problem.

    >>> solve_part1('test1.txt')
    20899048083289
    """
    logging.debug(f'EXECUTING SOLVE - 1')
    tiles, side_length, all_ids = read_input(filepath)

    tiles = {i: get_permutations(tiles[i]) for i in tiles}
    all_tiles = []
    for i in tiles:
        for perm in tiles[i]:
            all_tiles.append((i, perm))

    for tile in all_tiles:
        remaining = all_ids.copy()
        remaining.remove(tile[0])
        possible_image = assemble_image(tile, all_tiles, remaining, side_length)

        if possible_image is not None:
            return possible_image[0][0][0] * possible_image[0][-1][0] * \
                   possible_image[-1][0][0] * possible_image[-1][-1][0]

    return -1


def get_permutations(tile: List[str]) -> List[List[str]]:
    """Populates self.permutations with a list of all the possible permutations of this Tile.

    List contains this Tile and its permutations in the following order:
        0. this Tile
        1. this Tile horizontally flipped
        2. this Tile vertically flipped
        3. this Tile rotated right 90 degrees
        4. this Tile rotated right 180 degrees
        5. this Tile rotated 270 degrees
        6. this Tile horizontally flipped and rotated right 90 degrees
        7. this Tile horizontally flipped and rotated right 270 degrees
    """
    permutations = [tile.copy(), flip_horizontal(tile), flip_vertical(tile)]
    permutations.append(rotate_clockwise(tile))
    permutations.append(rotate_clockwise(permutations[-1]))
    permutations.append(rotate_clockwise(permutations[-1]))
    permutations.append(rotate_clockwise(permutations[1]))
    permutations.append(rotate_clockwise(permutations[2]))

    assert len(permutations) == 8
    assert all(permutations[i] != permutations[j]
               for i in range(len(permutations))
               for j in range(len(permutations))
               if i != j)
    return permutations


def flip_horizontal(tile: List[str]) -> List[str]:
    """Return a new Tile that is the horizontal flip of this tile.

    Horizontal flipping is done such that the left edge of this tile becomes the right edge
    of the new Tile.

    >>> t = ['abc', 'def', 'ghi']
    >>> y = flip_horizontal(t)
    >>> y
    ['cba', 'fed', 'ihg']
    """
    new_data = []
    for row in tile:
        new_data.append(row[::-1])

    return new_data


def flip_vertical(tile: List[str]) -> List[str]:
    """Return a new Tile that is the vertical flip of this tile.

    Vertical flipping is done such that the top edge of this tile becomes the bottom edge
    of the new Tile.

    >>> t = ['abc', 'def', 'ghi']
    >>> y = flip_vertical(t)
    >>> y
    ['ghi', 'def', 'abc']
    """
    return tile[::-1]


def rotate_clockwise(tile: List[str]) -> List[str]:
    """Return a new Tile that is this Tile rotated 90 degrees clockwise.

    >>> t = ['abc', 'def', 'ghi']
    >>> y = rotate_clockwise(t)
    >>> y
    ['gda', 'heb', 'ifc']
    >>> y is not t
    True
    """
    new_data = []
    for i in range(len(tile[0])):  # columns
        new_row_str = ''
        for j in range(len(tile) - 1, -1, -1):  # rows
            new_row_str += tile[j][i]
        new_data.append(new_row_str)

    return new_data


def assemble_image(tile: Tuple[int, List[str]], all_tiles: List[Tuple[int, List[str]]],
                   all_ids: Set[int], side_length: int) -> Optional[List[List[List[str]]]]:
    """Using the given tile as the top left tile in the grid of side_length by side_length, try to
    assemble the original image by matching edges. Returns -1 if grid is not possible.
    """
    grid = [[None for _ in range(side_length)] for _ in range(side_length)]
    grid[0][0] = tile

    if assemble_grid(grid, all_tiles, all_ids, 1):
        return grid
    else:
        return None


def assemble_grid(grid: List[List[Optional[Tuple[int, List[str]]]]],
                  all_tiles: List[Tuple[int, List[str]]],
                  remaining: Set[int],
                  i: int) -> bool:
    """Return True if grid gets filled correctly, False otherwise.
    """
    if i >= len(grid) * len(grid[0]):
        return True

    cartesian_index = (i // len(grid), i % len(grid[0]))
    for tile in all_tiles:
        if tile[0] in remaining:
            grid[cartesian_index[0]][cartesian_index[1]] = tile
            remaining.remove(tile[0])
            if check_top_left(grid, cartesian_index):
                possible = assemble_grid(grid, all_tiles, remaining, i + 1)
                if possible:
                    return True
            remaining.add(tile[0])

    return False


def check_top_left(grid: List[List[Optional[Tuple[int, List[str]]]]],
                   cartesian_index: Tuple[int, int]) -> bool:
    """Return whether the tile at the given cartesian index fits with the top and left tiles.
    """
    top_check = left_check = True
    if cartesian_index[0] > 0:
        check_tile = grid[cartesian_index[0] - 1][cartesian_index[1]]
        current_tile = grid[cartesian_index[0]][cartesian_index[1]]
        top_check = all(check_tile[1][-1][i] == current_tile[1][0][i] for i in range(len(check_tile[1][0])))
    if cartesian_index[1] > 0:
        check_tile = grid[cartesian_index[0]][cartesian_index[1] - 1]
        current_tile = grid[cartesian_index[0]][cartesian_index[1]]
        left_check = all(check_tile[1][i][-1] == current_tile[1][i][0] for i in range(len(check_tile[1])))
    return top_check and left_check


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 20 Part 2 problem.

    >>> solve_part2('test1.txt')
    273
    """
    logging.debug(f'EXECUTING SOLVE - 2')
    tiles, side_length, all_ids = read_input(filepath)

    tiles = {i: get_permutations(tiles[i]) for i in tiles}
    all_tiles = []
    for i in tiles:
        for perm in tiles[i]:
            all_tiles.append((i, perm))

    image = []
    for tile in all_tiles:
        remaining = all_ids.copy()
        remaining.remove(tile[0])
        possible_image = assemble_image(tile, all_tiles, remaining, side_length)

        if possible_image is not None and image == []:
            image = generate_full_image(possible_image)

    orientated_image = reorient_image(image)
    assert orientated_image != [], 'Monster not found in image.'

    for row_num in range(len(orientated_image) - 2):
        for col_num in range(len(orientated_image[row_num]) - 19):
            if is_monster(orientated_image, row_num, col_num, {'#', 'O'}):
                mark_monster(orientated_image, row_num, col_num)

    return sum(sum(c == '#' for c in r) for r in orientated_image)


def generate_full_image(grid: List[List[List[str]]]) -> List[str]:
    """Return the full generated image when removing image borders.
    """
    image = []
    for tile_row in range(len(grid)):
        for row_num in range(1, len(grid[tile_row][0][1]) - 1):
            full_row = ''
            for tile_col in range(len(grid[tile_row])):
                full_row += grid[tile_row][tile_col][1][row_num][1:-1]
            image.append(full_row)
    return image


def reorient_image(image: List[str]) -> List[str]:
    """Returns image in correct orientation to count monsters.
    """
    permutations = get_permutations(image)
    for perm in permutations:
        if check_for_monster(perm):
            return perm

    return []


def check_for_monster(image: List[str]) -> bool:
    """Return whether a monster can be found in the given image.

    >>> check_for_monster(['                  # ', '#    ##    ##    ###', ' #  #  #  #  #  #   '])
    True
    """
    i = 0  # top left corner of monster
    while i < len(image) - 2:
        j = 0
        while j < len(image[0]) - 18:
            if is_monster(image, i, j):
                return True
            j += 1
        i += 1

    return False


def is_monster(image: List[str], x: int, y: int, monster_char: Union[str, Set[str]] = '#') -> bool:
    """Return whether there is a monster at the given x and y coordinates.

    monster_char should be a set of monster characters or a single character.

    >>> test_image = ['.####...#####..#...###..', '#####..#..#.#.####..#.#.',
    ...               '.#.#...#.###...#.##.##..','#.#.##.###.#.##.##.#####']
    >>> is_monster(test_image, 0, 0, {'#', 'O'})
    False
    >>> test_image = ['.#.#...#.###...#.##.##..', '#.#.##.###.#.##.##.#####', '..##.###.####..#.####.##']
    >>> is_monster(test_image, 0, 2, {'#', 'O'})
    True
    """
    if isinstance(monster_char, str):
        return all(all(image[x + r][y + MONSTER[r][c]] == monster_char
                       for c in range(len(MONSTER[r])))
                   for r in range(len(MONSTER)))
    elif isinstance(monster_char, set):
        return all(all(image[x + r][y + MONSTER[r][c]] in monster_char
                       for c in range(len(MONSTER[r])))
                   for r in range(len(MONSTER)))


def mark_monster(image: List[str], row: int, col: int) -> None:
    """Mutate the given image and the monster at indices (row, col) to mark possible monster pixels.

    Marked monsters are denoted with an 'O'.

    >>> test_image = ['                  # ', '#    ##    ##    ###', ' #  #  #  #  #  #   ']
    >>> mark_monster(test_image, 0, 0)
    >>> test_image
    ['                  O ', 'O    OO    OO    OOO', ' O  O  O  O  O  O   ']
    >>> test_image = ['.#.#...#.###...#.##.##..', '#.#.##.###.#.##.##.#####', '..##.###.####..#.####.##']
    >>> mark_monster(test_image, 0, 2)
    >>> test_image
    ['.#.#...#.###...#.##.O#..', '#.O.##.OO#.#.OO.##.OOO##', '..#O.#O#.O##O..O.#O##.##']
    """
    for r in range(len(MONSTER)):
        image_row = list(image[row + r])
        for c in MONSTER[r]:
            image_row[col + c] = 'O'
        image[row + r] = ''.join(image_row)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D20P1: {solve_part1("input.txt")}')
    print(f'D20P2: {solve_part2("input.txt")}')
