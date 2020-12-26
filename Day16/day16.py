""" ADVENT OF CODE 2020 - DAY 16 - RAYMOND LI """

from __future__ import annotations

import logging
from typing import Dict, List, Set, Tuple


def read_input(filepath: str) -> Tuple[Dict[str, List[range]], List[List[str]], List[int]]:
    """Return processed version of the puzzle input.

    Returned tuple is in the format of: (rules, nearby tickets, my ticket)
    """
    with open(filepath) as input_file:
        all_input = input_file.read().strip().split('\n\n')

    rules = all_input[0].split('\n')
    rules = [r.split(': ') for r in rules]
    rules = {k: v.split(' or ') for k, v in rules}
    for k in rules:
        rules[k] = [r.split('-') for r in rules[k]]
        rules[k] = [range(int(rules[k][i][0]), int(rules[k][i][1]) + 1) for i in range(len(rules[k]))]

    nearby_tickets = all_input[2].split('\n')[1:]
    nearby_tickets = [t.split(',') for t in nearby_tickets]

    my_ticket = all_input[1].split('\n')[1].split(',')
    my_ticket = [int(val) for val in my_ticket]

    return (rules, nearby_tickets, my_ticket)


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 16 Part 1 problem.

    >>> solve_part1('test1.txt')
    71
    """
    logging.debug(f'EXECUTING SOLVE - 1')
    rules, nearby_tickets, _ = read_input(filepath)

    scanning_error_rate = 0
    for ticket in nearby_tickets:
        for val in ticket:
            val = int(val)
            if not in_rules(val, rules):
                scanning_error_rate += val

    return scanning_error_rate


def in_rules(value: int, rules: Dict[str, List[range]]) -> bool:
    """Return whether the value is a value for any of the rules.

    >>> test_rules = {'class': [range(1, 4), range(5, 8)],
    ...     'row': [range(6, 12), range(33, 45)],
    ...     'seat': [range(13, 41), range(45, 51)]}
    ...
    >>> in_rules(1, test_rules)
    True
    >>> in_rules(44, test_rules)
    True
    >>> in_rules(4, test_rules)
    False
    >>> in_rules(52, test_rules)
    False
    """
    for rule in rules:
        for defined_range in rules[rule]:
            if value in defined_range:
                return True

    return False


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 16 Part 2 problem.
    """
    logging.debug(f'EXECUTING SOLVE - 2')
    rules, nearby_tickets, my_ticket = read_input(filepath)

    valid_tickets = []  # List[List[str]]
    for ticket in nearby_tickets:
        if values_in_rules(ticket, rules):
            valid_tickets.append(ticket)

    columns = []  # List[Set[int]]
    for i in range(len(valid_tickets[0])):
        columns.append(set())
        for ticket in valid_tickets:
            columns[i].add(int(ticket[i]))

    col_rules = []  # List[List[str]]
    for col in columns:
        col_rules.append(col_follows_which_rules(col, rules))

    rule_cols = ['NA' for _ in col_rules]
    for _ in range(len(col_rules)):
        i = get_col_with_x_possible(col_rules, 1)
        rule_cols[i] = col_rules[i][0]
        remove_all_instances(rule_cols[i], col_rules)

    product = 1
    for i in range(len(rule_cols)):
        if rule_cols[i].startswith('departure'):
            product *= my_ticket[i]

    return product


def values_in_rules(ticket: List[str], rules: Dict[str, List[range]]) -> bool:
    """Returns True when this ticket follows the given rules, False otherwise.
    """
    for val in ticket:
        val = int(val)
        if not in_rules(val, rules):
            return False

    return True


def col_follows_which_rules(col: Set[int], rules: Dict[str, List[range]]) -> List[str]:
    """Returns the possible rules that all the values in the column follow.
    """
    possible_rules = []
    for rule in rules:
        if all(value_follows_rules(val, rules[rule]) for val in col):
            possible_rules.append(rule)

    return possible_rules


def value_follows_rules(value: int, rule: List[range]) -> bool:
    """Return whether the given value follows the given rule.

    >>> value_follows_rules(10, [range(0, 5), range(10, 15)])
    True
    >>> value_follows_rules(200, [range(10, 50), range(100, 200)])
    False
    """
    for defined_range in rule:
        if value in defined_range:
            return True

    return False


def get_col_with_x_possible(columns: List[List[str]], x: int) -> int:
    """Return the index that has x items.

    Preconditions:
        - len([col for columns if len(col) == x]) == 1
    """
    for i in range(len(columns)):
        if len(columns[i]) == x:
            return i

    raise ValueError(f'Column with {x} items not found.')


def remove_all_instances(value: str, columns: List[List[str]]) -> None:
    """Removes all instances of value in columns.
    """
    logging.debug(f'REMOVING {value}')
    for col in columns:
        try:
            col.remove(value)
        except ValueError:
            logging.debug(f'{value} not found in {col}')


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D16P1: {solve_part1("input.txt")}')
    print(f'D16P2: {solve_part2("input.txt")}')
