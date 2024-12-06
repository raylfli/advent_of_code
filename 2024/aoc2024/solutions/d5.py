"""
Advent of Code - Day 5: Print Queue
"""

from collections import defaultdict
from functools import reduce


def _parse_rules_updates(s: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    """
    Parse the input string into rules and page updates.
    """
    rules, updates = s.split('\n\n', maxsplit=1)

    # parse rules
    rules = [rule.strip().split('|') for rule in rules.strip().split('\n')]
    rules = [(int(rule[0]), int(rule[1])) for rule in rules]

    # parse updates
    updates = [[int(page.strip()) for page in update.strip().split(',')] for update in updates.strip().split('\n')]

    return rules, updates


def _check_update(rules: list[tuple[int, int]], update: list[int]) -> bool:
    """
    Check whether the update is valid given the rules.
    """
    update_indices = {v: i for i, v in enumerate(update)}

    for a, b in rules:
        if a not in update_indices or b not in update_indices:
            continue

        if update_indices[a] > update_indices[b]:
            return False

    return True


def _topological_sort(rules: list[tuple[int, int]], update: list[int]) -> list[int]:
    """
    Topologically sort the vertices in `update` given the edges in `rules`.

    Topological sort uses Kahn's algorithm.
    """
    # set up sort data structures
    nodes = set(update)
    rules_dict = defaultdict(set)
    no_incoming = set(update)
    for a, b in rules:
        if a in nodes and b in nodes:
            rules_dict[a].add(b)
            if b in no_incoming:
                no_incoming.remove(b)

    # sort pages in update
    order = []
    while len(no_incoming) > 0:
        n = no_incoming.pop()
        order.append(n)

        for m in list(rules_dict[n]):
            rules_dict[n].remove(m)
            if m not in reduce(lambda x, y: x.union(y), rules_dict.values()):
                no_incoming.add(m)

    return order


def solve_part1(s: str) -> int:
    """
    Solve AoC D5 P1.
    """
    rules, updates = _parse_rules_updates(s)

    total = 0
    for update in updates:
        if _check_update(rules, update):
            total += update[len(update) // 2]

    return total


def solve_part2(s: str) -> int:
    """
    Solve AoC D5 P2.
    """
    rules, updates = _parse_rules_updates(s)

    total = 0
    for update in updates:
        if not _check_update(rules, update):
            fixed = _topological_sort(rules, update)
            total += fixed[len(fixed) // 2]

    return total
