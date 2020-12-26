""" ADVENT OF CODE 2020 - DAY 23 - RAYMOND LI """

from __future__ import annotations

import logging
from typing import Dict, List, Tuple


def read_input(filepath: str) -> List[int]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        cups_input = input_file.read().strip()

    return [int(c) for c in cups_input]


def generate_linked_dictionary(cups_input: List[int]) -> Dict[int, int]:
    """Return generated singly linked dictionary structure.
    """
    cups = {cups_input[0]: cups_input[1]}
    for c in range(1, len(cups_input)):
        cups[cups_input[c - 1]] = cups_input[c]

    cups[cups_input[-1]] = cups_input[0]
    return cups


def solve_part1(filepath: str, moves: int) -> str:
    """Returns solution to Day 23 Part 1 problem.

    >>> solve_part1('test1.txt', 10)
    '92658374'
    >>> solve_part1('test1.txt', 100)
    '67384529'
    """
    logging.debug(f'EXECUTING SOLVE - 1')
    cups_input = read_input(filepath)
    cups = generate_linked_dictionary(cups_input)

    min_cup, max_cup = min(cups), max(cups)
    current = cups_input[0]
    for _ in range(moves):
        current = move_cups(cups, current, min_cup, max_cup)

    return get_cups_string(cups, 1)


def solve_part2(filepath: str, moves: int) -> int:
    """Returns solution to Day 23 Part 2 problem.
    """
    logging.debug(f'EXECUTING SOLVE - 2')
    cups_input = read_input(filepath)
    max_cup = max(cups_input)
    cups_input.extend(range(max_cup + 1, 1000001))
    cups = generate_linked_dictionary(cups_input)

    min_cup, max_cup = 1, 1000000
    current = cups_input[0]
    for _ in range(moves):
        current = move_cups(cups, current, min_cup, max_cup)

    first = cups[1]
    second = cups[first]

    return first * second


def move_cups(cups: Dict[int, int], current: int, min_cup: int, max_cup: int) -> int:
    """Move cups based on the crab's instructions.

    Returns the new current cup.
    """
    first_picked, picked_up = pickup_cups(cups, current)
    destination = get_destination_cup(current, picked_up, min_cup, max_cup)
    place_cups(cups, picked_up, first_picked, destination)
    return cups[current]


def pickup_cups(cups: Dict[int, int], current: int) -> Tuple[int, Dict[int, int]]:
    """Return a tuple of the first picked up cup and a dictionary of the three picked up cups.

    Mutates the the dictionary of cups.
    """
    picked = {}
    cup = cups[current]
    first_picked = cup
    for _ in range(3):
        picked[cup] = cups[cup]
        cup = cups[cup]
    cups[current] = cup
    return (first_picked, picked)


def get_destination_cup(current: int, picked_up: Dict[int, int], min_cup: int, max_cup: int) -> int:
    """Return destination cup based on the current and picked up cups.
    """
    target = current - 1
    while target in picked_up or target < min_cup:
        if target < min_cup:
            target = max_cup
        else:
            target -= 1

    return target


def place_cups(cups: Dict[int, int], picked_up: Dict[int, int], picked_first: int, destination: int) -> None:
    """Place the picked up cups directly after the destination cup.
    """
    last_cup_picked = picked_first
    for _ in range(len(picked_up) - 1):
        last_cup_picked = picked_up[last_cup_picked]
    cups[last_cup_picked] = cups[destination]
    cups[destination] = picked_first


def get_cups_string(cups: Dict[int, int], start_num: int) -> str:
    """Get the string representing of the given cups.

    String starts from the the cup after the given start number.
    """
    cup = cups[start_num]
    s = []
    while cup != start_num:
        s.append(str(cup))
        cup = cups[cup]

    return ''.join(s)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D23P1: {solve_part1("input.txt", 100)}')
    print(f'D23P2: {solve_part2("input.txt", 10000000)}')
