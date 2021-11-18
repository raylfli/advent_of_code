""" ADVENT OF CODE 2020 - DAY 2 - RAYMOND LI """

from __future__ import annotations

from typing import List, Tuple


def read_input(filepath: str) -> Tuple[List[str], List[str], List[Tuple[int, int]]]:
    """Return processed version of the puzzle input.

    Returned tuple contains lists of the same length in the format:
        (passwords, required letters, required occurrences)
    """
    with open(filepath) as input_file:
        lines = [line.split(':') for line in input_file.read().strip().split('\n')]

    policies = [line[0] for line in lines]
    passwords = [line[1] for line in lines]

    policy_parts = [policy.split(' ') for policy in policies]
    policy_range = [tuple(policy[0].split('-', 1)) for policy in policy_parts]
    policy_letter = [policy[1] for policy in policy_parts]

    return (passwords, policy_letter, policy_range)


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 2 Part 1 problem.
    """
    passwords, policy_letters, policy_ranges = read_input(filepath)

    count_valid = 0
    for i in range(len(passwords)):
        if int(policy_ranges[i][0]) <= passwords[i].count(policy_letters[i]) <= int(policy_ranges[i][1]):
            count_valid += 1

    return count_valid


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 2 Part 2 problem.
    """
    passwords, policy_letters, policy_ranges = read_input(filepath)

    count_valid = 0
    for i in range(len(passwords)):
        first_occur = policy_letters[i] == passwords[i][int(policy_ranges[i][0])]
        second_occur = policy_letters[i] == passwords[i][int(policy_ranges[i][1])]
        if first_occur ^ second_occur:
            count_valid += 1

    return count_valid


if __name__ == '__main__':
    print(f'D2P1: {solve_part1("input.txt")}')
    print(f'D2P2: {solve_part2("input.txt")}')
