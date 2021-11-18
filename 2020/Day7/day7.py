""" ADVENT OF CODE 2020 - DAY 7 - RAYMOND LI """

from __future__ import annotations

import re
from typing import Dict, Optional


def read_input(filepath: str) -> Dict[str, Optional[Dict[str, int]]]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        rules = input_file.read().strip().split('.\n')

    bags_rules = {}  # Dict[str, Optional[Dict[str, int]]]
    for rule in rules:
        bag_rule = rule.split(' contain ')
        contents = bag_rule[1].split(', ')

        possible_contents = {}  # Optional[Dict[str, int]]
        if re.match(r'no other bags', contents[0]):
            possible_contents = None
        else:
            for content in contents:
                content = content.split(' ', 1)
                possible_contents[content[1].rstrip('s').rstrip(' bag')] = int(content[0])

        bags_rules[bag_rule[0].rstrip('s').rstrip(' bag')] = possible_contents

    return bags_rules


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 7 Part 1 problem.

    >>> solve_part1('test1.txt')
    4
    """
    bags_rules = read_input(filepath)

    eventual_shiny_golds = 0
    for bag in bags_rules:
        if has_shiny_gold(bags_rules, bag):
            eventual_shiny_golds += 1

    return eventual_shiny_golds


def has_shiny_gold(all_rules: Dict[str, Optional[Dict[str, int]]], bag: str) -> bool:
    """Returns whether the bag eventually has a shiny gold bag as a possible content.

    Recursively checks other bags.

    Preconditions:
        - bag in all_rules
    """
    if all_rules[bag] is None:
        return False
    elif 'shiny gold' in all_rules[bag]:
        return True

    return any(has_shiny_gold(all_rules, b) for b in all_rules[bag])


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 7 Part 2 problem.

    >>> solve_part2('test2.txt')
    126
    """
    bags_rules = read_input(filepath)

    return bag_count(bags_rules, 'shiny gold')


def bag_count(all_rules: Dict[str, Optional[Dict[str, int]]], bag: str) -> int:
    """Returns number of bags within the specified bag.

    Recursively moves through bag nodes.
    """
    if all_rules[bag] is None:
        return 0
    else:
        return sum(all_rules[bag][b] + all_rules[bag][b] * bag_count(all_rules, b)
                   for b in all_rules[bag])


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print(f'D7P1: {solve_part1("input.txt")}')
    print(f'D7P2: {solve_part2("input.txt")}')
