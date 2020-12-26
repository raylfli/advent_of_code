""" ADVENT OF CODE 2020 - DAY 19 - RAYMOND LI """

from __future__ import annotations

import logging
import re
from typing import Dict, List, Tuple

RE_DIGITS = re.compile(r'\d+')


def read_input(filepath: str) -> Tuple[Dict[int, str], List[str]]:
    """Return processed version of the puzzle input.

    Returned tuple is in the format of: (rules, messages)
    """
    with open(filepath) as input_file:
        parts = input_file.read().strip().split('\n\n')

    rules = [part.split(':') for part in parts[0].split('\n')]
    return ({int(num): rule.lstrip(' ').replace('"', '') for num, rule in rules}, parts[1].split('\n'))


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 19 Part 1 problem.

    >>> solve_part1('test1.txt')
    2
    >>> solve_part1('test2.txt')
    3
    """
    logging.debug(f'EXECUTING SOLVE - 1')
    rules, messages = read_input(filepath)
    parse_rule(rules, 0)  # 0th rule entry point

    match_pattern = re.compile(rules[0])
    return sum(1 for message in messages if re.fullmatch(match_pattern, message))


def parse_rule(rules: Dict[int, str], rule: int) -> str:
    """Parse the given rule into a valid regular expression string and mutate the list of rules.

    Recursively evaluates required nested rules.
    """
    if len(rules[rule]) == 1 or not re.match(RE_DIGITS, rules[rule]):
        return rules[rule]
    else:
        regex_str = '('
        for char in rules[rule].split(' '):
            if char != '|':
                regex_str += parse_rule(rules, int(char))
            else:
                regex_str += '|'
        regex_str += ')'
        rules[rule] = regex_str
        return regex_str


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 19 Part 2 problem.

    >>> solve_part2('test2.txt')
    12
    """
    logging.debug(f'EXECUTING SOLVE - 2')
    rules, messages = read_input(filepath)

    rules[8] = '42 | 42 8'
    rules[11] = '42 31 | 42 11 31'

    parse_rule_part2(rules, 0)  # 0th rule entry point

    patterns = generate_num_patterns(rules[0], 4)

    match_patterns = [re.compile(pattern) for pattern in patterns]
    return sum(1 for message in messages
               if any(re.fullmatch(pattern, message)
                      for pattern in match_patterns))


def parse_rule_part2(rules: Dict[int, str], rule: int) -> str:
    """Parse the given rule into a valid regular expression string and mutate the list of rules.

    Recursively evaluates required nested rules.
    """
    if len(rules[rule]) == 1 or not re.search(RE_DIGITS, rules[rule]):
        return rules[rule]
    elif rule == 8:
        regex_str = f'({parse_rule_part2(rules, 42)}|{parse_rule_part2(rules, 42)}+)'
        rules[rule] = regex_str
        return regex_str
    elif rule == 11:
        regex_str = f'({parse_rule_part2(rules, 42)}{parse_rule_part2(rules, 31)}|' \
                    f'{parse_rule_part2(rules, 42)}{{%NUM_REP%}}{parse_rule_part2(rules, 31)}{{%NUM_REP%}})'
        rules[rule] = regex_str
        return regex_str
    else:
        regex_str = '('
        for char in rules[rule].split(' '):
            if char != '|':
                regex_str += parse_rule_part2(rules, int(char))
            else:
                regex_str += '|'
        regex_str += ')'
        rules[rule] = regex_str
        return regex_str


def generate_num_patterns(pattern: str, max_rep: int = 10) -> List[str]:
    """Return list of regex patterns with all '%NUM_REP%' occurrences replaced with increasing
    numbers.

    max_rep specifies the highest number of repetitions of the patterns in the returned list.

    Returned list will be of length max_rep.

    >>> generate_num_patterns('abcd{%NUM_REP%}', 3)
    ['abcd{1}', 'abcd{2}', 'abcd{3}']
    >>> generate_num_patterns('ab{%NUM_REP%}cd{%NUM_REP%}', 3)
    ['ab{1}cd{1}', 'ab{2}cd{2}', 'ab{3}cd{3}']
    """
    patterns = []
    for i in range(1, max_rep + 1):
        patterns.append(pattern.replace('%NUM_REP%', str(i)))

    return patterns


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D19P1: {solve_part1("input.txt")}')
    print(f'D19P2: {solve_part2("input.txt")}')
