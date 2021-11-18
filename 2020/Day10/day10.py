""" ADVENT OF CODE 2020 - DAY 10 - RAYMOND LI """

from __future__ import annotations

from typing import List, Set


def read_input(filepath: str) -> List[int]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        nums = input_file.read().strip().split('\n')

    nums = [int(n) for n in nums]
    nums.sort()
    return nums


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 10 Part 1 problem.

    >>> solve_part1('test1.txt')
    35
    >>> solve_part1('test2.txt')
    220
    """
    nums = read_input(filepath)

    one_diff = 1  # charger has rating of 0 and first adapter is 1
    three_diff = 1  # device has rating +3 of last (last is 19)
    for i in range(len(nums) - 1):
        diff = nums[i + 1] - nums[i]
        if diff == 1:
            one_diff += 1
        elif diff == 3:
            three_diff += 1

    return one_diff * three_diff


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 10 Part 2 problem.

    >>> solve_part2('test1.txt')
    8
    >>> solve_part2('test2.txt')
    19208
    """
    nums = read_input(filepath
                      )
    device_end = nums[-1] + 3
    nums_set = set(nums)

    return memorized_sum_branches(nums_set, 0, device_end)


def memorized_sum_branches(all_nums: Set[int], start_num: int, max_num: int) -> int:
    """Recursively counts number of possible branches with memorization.
    """
    branches = [-1 for _ in range(max_num)]

    return sum_branches(all_nums, start_num, max_num, branches)


def sum_branches(all_nums: Set[int], start_num: int, max_num: int, cached_branches: List[int]) -> int:
    """Recursively counts number of possible branches.
    """
    if start_num + 3 == max_num:
        return 1

    if cached_branches[start_num] == -1:
        jumps = [None, None, None]
        if start_num + 1 in all_nums:
            jumps[0] = sum_branches(all_nums, start_num + 1, max_num, cached_branches)

        if start_num + 2 in all_nums:
            jumps[1] = sum_branches(all_nums, start_num + 2, max_num, cached_branches)

        if start_num + 3 in all_nums:
            jumps[2] = sum_branches(all_nums, start_num + 3, max_num, cached_branches)

        cached_branches[start_num] = sum([jump for jump in jumps if jump is not None])

    return cached_branches[start_num]


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print(f'D10P1: {solve_part1("input.txt")}')
    print(f'D10P2: {solve_part2("input.txt")}')
