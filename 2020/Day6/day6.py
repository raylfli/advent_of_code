""" ADVENT OF CODE 2020 - DAY 6 - RAYMOND LI """

from __future__ import annotations

from typing import List


def read_input(filepath: str) -> List[str]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        return input_file.read().strip().split('\n\n')


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 6 Part 1 problem.
    """
    groups = read_input(filepath)

    groups_yes = []  # List[Set[str]]
    group_sums = []  # List[int]
    for group in groups:
        group = group.replace('\n', '').replace(' ', '')
        groups_yes.append({question for question in group})
        group_sums.append(len(groups_yes[-1]))

    return sum(group_sums)


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 6 Part 2 problem.

    >>> solve_part2('test.txt')
    6
    """
    groups = read_input(filepath)

    group_sums = []  # List[int]
    for group in groups:
        people = group.replace(' ', '').split('\n')  # List[str]
        counts = {}  # Dict[str, int]
        for person in people:
            for c in person:
                if c in counts:
                    counts[c] += 1
                else:
                    counts[c] = 1

        group_sums.append(len([c for c in counts if counts[c] == len(people)]))

    return sum(group_sums)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print(f'D6P1: {solve_part1("input.txt")}')
    print(f'D6P2: {solve_part2("input.txt")}')
