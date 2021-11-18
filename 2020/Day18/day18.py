""" ADVENT OF CODE 2020 - DAY 18 - RAYMOND LI """

from __future__ import annotations

import logging
import queue
from typing import Any, Dict, List, Union


def read_input(filepath: str) -> List[str]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        return input_file.read().strip().split('\n')


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 18 Part 1 problem.

    >>> solve_part1('test1.txt')
    26
    >>> solve_part1('test2.txt')
    437
    >>> solve_part1('test3.txt')
    12240
    >>> solve_part1('test4.txt')
    13632
    >>> solve_part1('test5.txt')
    71
    >>> solve_part1('test6.txt')
    51
    """
    logging.debug(f'EXECUTING SOLVE - 1')
    lines = read_input(filepath)

    operators = {'+': 1,
                 '*': 1}

    sums = []
    for line in lines:
        sums.append(solve_line(line, operators))

    return sum(int(s) for s in sums)


def solve_line(line: str, operators: Dict[str, int]) -> int:
    """Return the result of one mathematical line.

    Operators should be a dictionary mapping operators to their precedence.

    >>> solve_line('(1 + 3) * ((3 * 7) + 2)', {'*': 1, '+': 2})
    92
    """
    input_tokens = queue.Queue()
    line = list(line)
    for c in line:
        if c != ' ':
            input_tokens.put(c)

    rpn = shunting_yard(input_tokens, operators)
    return rpn_solve(rpn)


def shunting_yard(s: queue.Queue, operators: Dict[str, int]) -> queue.Queue:
    """Return the Reverse Polish Notation representation of the input string.

    Operators should be a dictionary mapping operators to their precedence.
    """
    output_queue = queue.Queue()
    operator_stack = queue.LifoQueue()
    top_oper_stack = None
    while not s.empty():
        value = s.get()

        if value.isdigit():
            output_queue.put(value)
        elif value in {'*', '+'}:
            while top_oper_stack is not None and \
                    top_oper_stack != '(' and \
                    operators[top_oper_stack] >= operators[value]:
                output_queue.put(operator_stack.get())
                top_oper_stack = stack_peep(operator_stack)
            operator_stack.put(value)
            top_oper_stack = value
        elif value == '(':
            operator_stack.put(value)
            top_oper_stack = value
        elif value == ')':
            while top_oper_stack != '(':
                output_queue.put(operator_stack.get())
                top_oper_stack = stack_peep(operator_stack)
            if top_oper_stack == '(':
                operator_stack.get()
                top_oper_stack = stack_peep(operator_stack)

    while not operator_stack.empty():
        output_queue.put(operator_stack.get())

    return output_queue


def stack_peep(s: queue.LifoQueue) -> Any:
    """Return the last item in the stack.

    Returns None if the stack is empty.
    """
    if s.empty():
        return None
    else:
        value = s.get()
        s.put(value)
        return value


def rpn_solve(inp: queue.Queue) -> int:
    """Return the solved Reverse Polish Notation representation of the given input queue.
    """
    stack = queue.LifoQueue()
    while not inp.empty():
        value = inp.get()
        if value.isdigit():
            stack.put(value)
        else:
            a = stack.get()
            b = stack.get()
            stack.put(str(solve_operation(b, value, a)))

    return int(stack.get())


def solve_operation(a: Union[int, str], oper: str, b: Union[int, str]) -> int:
    """Return the solution of one operation. Operation is taken literally: a oper b

    So if a = 1, oper = -, b = 2: a oper b = 1 - 2 = -1

    Preconditions:
        - len(oper) == 1
        - oper in {'+', '-', '*', '/', '//'}
    """
    return eval(f'{a}{oper}{b}')


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 18 Part 2 problem.

    >>> solve_part2('test1.txt')
    46
    >>> solve_part2('test2.txt')
    1445
    >>> solve_part2('test3.txt')
    669060
    >>> solve_part2('test4.txt')
    23340
    >>> solve_part2('test5.txt')
    231
    >>> solve_part2('test6.txt')
    51
    """
    logging.debug(f'EXECUTING SOLVE - 2')
    lines = read_input(filepath)

    operators = {'+': 2,
                 '*': 1}

    sums = []
    for line in lines:
        sums.append(solve_line(line, operators))

    return sum(int(s) for s in sums)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D18P1: {solve_part1("input.txt")}')
    print(f'D18P2: {solve_part2("input.txt")}')
