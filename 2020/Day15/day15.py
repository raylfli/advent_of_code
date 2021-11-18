""" ADVENT OF CODE 2020 - DAY 15 - RAYMOND LI """

from __future__ import annotations

import logging
from typing import Dict, List, Tuple


def read_input(filepath: str) -> Tuple[List[int], Dict[int, int]]:
    """Return processed version of the puzzle input.

    Returned tuple is in the format: (numbers, numbers previous said)
    """
    with open(filepath) as input_file:
        starting_nums = input_file.read().strip().split(',')

    nums = [int(num) for num in starting_nums]
    said = {nums[i]: i for i in range(len(nums) - 1)}

    return (nums, said)


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 15 Part 1 problem.

    >>> solve_part1('test1.txt')
    436
    >>> solve_part1('test2.txt')
    1
    >>> solve_part1('test3.txt')
    10
    >>> solve_part1('test4.txt')
    27
    >>> solve_part1('test5.txt')
    78
    >>> solve_part1('test6.txt')
    438
    >>> solve_part1('test7.txt')
    1836
    """
    nums, said = read_input(filepath)
    return play_game(nums, said, 2020)


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 15 Part 2 problem.

    No test cases because this takes far too long to run.
    """
    nums, said = read_input(filepath)
    return play_game(nums, said, 30000000)


def play_game(nums: List[int], said: Dict[int, int], turns: int) -> int:
    """Complete the given number of turns in the memory game and return the last number spoken.

    The last spoken number will be the number spoken on the given final turn.
    """
    previous_num = nums[-1]
    for i in range(len(nums), turns):
        if previous_num not in said:
            said[previous_num] = i - 1
            previous_num = 0
        elif previous_num in said:
            new_num = i - 1 - said[previous_num]
            said[previous_num] = i - 1
            previous_num = new_num
        else:
            logging.warning(f'Something really weird happened.')

    return previous_num


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D15P1: {solve_part1("input.txt")}')
    print(f'D15P2: {solve_part2("input.txt")}')
