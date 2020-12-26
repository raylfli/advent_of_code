""" ADVENT OF CODE 2020 - DAY 9 - RAYMOND LI """

from __future__ import annotations

from typing import List


def read_input(filepath: str) -> List[int]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        nums = input_file.read().strip().split('\n')

    return [int(n) for n in nums]


def solve_part1(filepath: str, preamble_len: int) -> int:
    """Returns solution to Day 9 Part 1 problem.

    >>> solve_part1('test1.txt', 5)
    127
    """
    nums = read_input(filepath)

    for i in range(preamble_len, len(nums)):
        window = nums[i - preamble_len:i]
        if not sum_of_any(window, nums[i]):
            return nums[i]

    return -1


def sum_of_any(nums: List[int], num: int) -> bool:
    """Returns whether the given num can be written as the sum of
    any two unique numbers in nums.

    >>> sum_of_any([1, 2, 3, 4, 5, 23, 24, 25], 26)
    True
    >>> sum_of_any([1, 2, 3, 4, 5], 1)
    False
    """
    for n in nums:
        possible_match = num - n
        if possible_match != n and possible_match in nums:
            return True

    return False


def solve_part2(filepath: str, preamble_len: int) -> int:
    """Returns solution to Day 9 Part 2 problem.

    >>> solve_part2('test1.txt', 5)
    62
    """
    nums = read_input(filepath)

    num_to_find = solve_part1(filepath, preamble_len)
    ind_num_to_find = nums.index(num_to_find)

    for i in range(ind_num_to_find - 1):
        for j in range(2, ind_num_to_find - i):
            window = nums[i:i + j]
            if len(window) > 2 and sum_to_num(window, num_to_find):
                return min(window) + max(window)

    return -1


def sum_to_num(nums: List[int], num: int) -> bool:
    """Returns whether the sum of the numbers in nums is num.

    >>> sum_to_num([1, 4, 5], 10)
    True
    >>> sum_to_num([1, 2, 3, 4, 5], 4)
    False
    """
    total = 0
    for n in nums:
        total += n
        if total > num:
            return False

    return total == num


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print(f'D9P1: {solve_part1("input.txt", 25)}')
    print(f'D9P2: {solve_part2("input.txt", 25)}')
