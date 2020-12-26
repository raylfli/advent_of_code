""" ADVENT OF CODE 2020 - DAY 12 - RAYMOND LI """

from __future__ import annotations

import logging
from typing import List, Tuple

DIRECTIONS_LETTER = {'N': 90,
                     'E': 0,
                     'S': 270,
                     'W': 180}
DIRECTIONS_DEGREES = {90: 'N',
                      0: 'E',
                      270: 'S',
                      180: 'W'}


def read_input(filepath: str) -> List[str]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        return input_file.read().strip().split('\n')


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 12 Part 1 problem.

    >>> solve_part1('test1.txt')
    25
    """
    instructions = read_input(filepath)

    facing = 'E'
    x, y = 0, 0
    for instruction in instructions:
        direction = instruction[0]
        value = int(instruction[1:])

        logging.debug(f'({x}, {y}) -- {direction}: {value}')

        if direction == 'F':
            x, y = move_ship(x, y, facing, value)
        elif direction in {'L', 'R'}:
            facing = turn_ship(facing, direction, value)
        elif direction in {'N', 'S', 'E', 'W'}:
            x, y = move_ship(x, y, direction, value)
        else:
            logging.warning('Invalid movement command.')

    return abs(x) + abs(y)


def turn_ship(facing: str, direction: str, degrees: int) -> str:
    """Returns the new direction based on the current direction and the degrees.

    Preconditions:
        - len(facing) == 1
        - direction in {'L', 'R'}
        - degrees % 90 == 0
        - degrees >= 0

    >>> turn_ship('E', 'L', 90)
    'N'
    >>> turn_ship('W', 'R', 180)
    'E'
    """
    deg = DIRECTIONS_LETTER[facing]
    direc = 1 if direction == 'L' else -1

    deg += direc * degrees
    while deg < 0:
        deg += 360
    while deg >= 360:
        deg -= 360

    return DIRECTIONS_DEGREES[deg]


def move_ship(x: int, y: int, direction: str, value: int) -> Tuple[int, int]:
    """Return the new x and y incremented by the given direction and value.

    Preconditions:
        - len(direction) == 1
        - value >= 0
        - direction in {'N', 'S', 'E', 'W'}

    >>> move_ship(0, 0, 'N', 10)
    (0, 10)
    >>> move_ship(0, 0, 'S', 10)
    (0, -10)
    >>> move_ship(0, 0, 'W', 10)
    (-10, 0)
    """
    if direction == 'N':
        y += value
    elif direction == 'E':
        x += value
    elif direction == 'S':
        y -= value
    elif direction == 'W':
        x -= value
    else:
        logging.warning(f"Direction '{direction}' not valid.")

    return x, y


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 12 Part 2 problem.

    >>> solve_part2('test1.txt')
    286
    """
    instructions = read_input(filepath)

    facing = 'E'
    s_x, s_y = 0, 0  # ship
    w_x, w_y = s_x + 10, s_y + 1  # waypoint
    for instruction in instructions:
        direction = instruction[0]
        value = int(instruction[1:])

        logging.debug(f'(SHIP: {s_x}, {s_y}), WAY: ({w_x}, {w_y}) -- {direction}: {value}')

        if direction == 'F':
            for _ in range(value):
                s_x, s_y, w_x, w_y = move_ship_and_way(s_x, s_y, w_x, w_y)
        elif direction in {'L', 'R'}:
            facing, w_x, w_y = turn_ship_and_way(s_x, s_y, w_x, w_y, facing, direction, value)
        elif direction in {'N', 'S', 'E', 'W'}:
            w_x, w_y = move_way(w_x, w_y, direction, value)
        else:
            logging.warning('Invalid movement command.')

    return abs(s_x) + abs(s_y)


def turn_ship_and_way(s_x: int, s_y: int, w_x: int, w_y: int,
                      facing: str, direction: str, degrees: int) -> Tuple[str, int, int]:
    """Returns the new direction based on the current direction and the degrees.

    Returned tuple is in the format of: (ship_direction, way_x, way_y)

    Preconditions:
        - len(facing) == 1
        - direction in {'L', 'R'}
        - degrees % 90 == 0
        - degrees >= 0

    >>> turn_ship_and_way(0, 0, 10, 1, 'E', 'L', 90)
    ('N', -1, 10)
    >>> turn_ship_and_way(0, 0, 10, 1, 'W', 'R', 180)
    ('E', -10, -1)
    """
    deg = DIRECTIONS_LETTER[facing]
    direc = 1 if direction == 'L' else -1

    deg += direc * degrees
    logging.debug(f'deg: {deg}')

    way_offset_x = w_x - s_x
    way_offset_y = w_y - s_y

    turns = -1 * direc * degrees // 90  # positive for left, negative for right
    logging.debug(f'direc: {direc} -- degrees: {degrees} -- turns: {turns}')
    if turns > 0:
        for _ in range(turns):
            way_offset_x, way_offset_y = way_offset_y, -way_offset_x
    elif turns < 0:
        for _ in range(0, turns, -1):
            way_offset_x, way_offset_y = -way_offset_y, way_offset_x

    while deg < 0:
        deg += 360
    while deg >= 360:
        deg -= 360

    new_dir = DIRECTIONS_DEGREES[deg]

    return (new_dir, s_x + way_offset_x, s_y + way_offset_y)


def move_way(x: int, y: int, direction: str, value: int) -> Tuple[int, int]:
    """Return new x and y incremented by the given direction and value.

    Preconditions:
        - len(direction) == 1
        - value >= 0
        - direction in {'N', 'S', 'E', 'W'}

    >>> move_way(0, 0, 'N', 10)
    (0, 10)
    >>> move_way(0, 0, 'S', 10)
    (0, -10)
    >>> move_way(0, 0, 'W', 10)
    (-10, 0)
    """
    if direction == 'N':
        y += value
    elif direction == 'E':
        x += value
    elif direction == 'S':
        y -= value
    elif direction == 'W':
        x -= value
    else:
        logging.warning(f"Direction '{direction}' not valid.")

    return x, y


def move_ship_and_way(s_x: int, s_y: int, w_x: int, w_y: int) -> Tuple[int, int, int, int]:
    """Return the new ship and waypoint xs and ys computed by moving the ship to the waypoint.

    The returned tuple has the following format: (ship_x, ship_y, way_x, way_y)

    Preconditions:
        - len(direction) == 1
        - value >= 0
        - direction in {'N', 'S', 'E', 'W'}

    >>> move_ship_and_way(0, 0, 10, 1)
    (10, 1, 20, 2)
    >>> move_ship_and_way(0, 0, 5, -1)
    (5, -1, 10, -2)
    >>> move_ship_and_way(10, 1, 20, 2)
    (20, 2, 30, 3)
    """
    way_offset_x, way_offset_y = w_x - s_x, w_y - s_y
    s_x, s_y = w_x, w_y
    w_x, w_y = s_x + way_offset_x, s_y + way_offset_y

    return s_x, s_y, w_x, w_y


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D12P1: {solve_part1("input.txt")}')
    print(f'D12P2: {solve_part2("input.txt")}')
