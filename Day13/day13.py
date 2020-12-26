""" ADVENT OF CODE 2020 - DAY 13 - RAYMOND LI """

from __future__ import annotations

import logging
from typing import List, Union


def read_input(filepath: str) -> List[str]:
    """Return processed version of the puzzle input.

    Tuple is in the format: (earliest departure, set of bus numbers)
    """
    with open(filepath) as input_file:
        return input_file.read().strip().split('\n')


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 13 Part 1 problem.

    >>> solve_part1('test1.txt')
    295
    """
    input_strs = read_input(filepath)
    earliest_dep = int(input_strs[0])
    busses = {int(bus) for bus in input_strs[1].split(',') if bus != 'x'}

    possible_dep = earliest_dep
    while True:
        for bus in busses:
            if possible_dep % bus == 0:
                return bus * (possible_dep - earliest_dep)
        possible_dep += 1


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 13 Part 2 problem.

    >>> solve_part2('test1.txt')
    1068781
    """
    input_strs = read_input(filepath)

    busses = [int(bus) if bus.isdigit() else bus for bus in input_strs[1].split(',')]

    possible_timestamp = 0
    step = 1
    for i in range(len(busses)):
        if busses[i] != 'x':
            while (possible_timestamp + i) % busses[i] != 0:
                possible_timestamp += step
            step *= busses[i]
    return possible_timestamp


def check_times(possible_timestamp: int, busses: List[Union[int, str]]) -> bool:
    """Return whether the busses depart at their required offsets.

    >>> check_times(3417, [17, 'x', 13, 19])
    True
    >>> check_times(754018, [67, 7, 59, 61])
    True
    >>> check_times(779210, [67, 'x', 7, 59, 61])
    True
    >>> check_times(1261476, [67, 7, 'x', 59, 61])
    True
    >>> check_times(1202161486, [1789, 37, 47, 1889])
    True
    >>> check_times(3416, [17, 'x', 13, 19])
    False
    >>> check_times(754017, [67, 7, 59, 61])
    False
    >>> check_times(779209, [67, 'x', 7, 59, 61])
    False
    >>> check_times(1261475, [67, 7, 'x', 59, 61])
    False
    >>> check_times(1202161485, [1789, 37, 47, 1889])
    False
    """
    for bus in busses:
        if bus != 'x' and possible_timestamp % bus != 0:
            return False
        possible_timestamp += 1

    return True


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D13P1: {solve_part1("input.txt")}')
    print(f'D13P2: {solve_part2("input.txt")}')
