""" ADVENT OF CODE 2020 - DAY 8 - RAYMOND LI """

from __future__ import annotations

from typing import List, Optional, Set


def read_input(filepath: str) -> List[str]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        return input_file.read().strip().split('\n')


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 8 Part 1 problem.

    >>> solve_part1('test1.txt')
    5
    """
    instructions = read_input(filepath)

    accumulator = 0
    visited_instructions = set()
    i = 0
    while i not in visited_instructions:
        visited_instructions.add(i)
        instruction = instructions[i].split(' ')

        direction = 1 if instruction[1][0] == '+' else -1
        offset = int(instruction[1][1:])

        if instruction[0] == 'acc':
            accumulator += direction * offset
        elif instruction[0] == 'jmp':
            i += direction * offset
            i -= 1

        i += 1

    return accumulator


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 8 Part 2 problem.

    >>> solve_part2('test1.txt')
    8
    """
    instructions = read_input(filepath)

    return instruction_branch(instructions, set(), 0, 0, False)


def instruction_branch(instructions: List[str], visited: Set[int],
                       i: int, accumulator: int, changed: bool) -> Optional[int]:
    """Recursively traverses through different instruction choices.

    Returns accumulator value if the program terminates by getting to the end of the instructions,
    None if the program enters an infinite loop.
    """
    if i in visited:
        return None
    elif i >= len(instructions):
        return accumulator

    visited = visited.copy()
    visited.add(i)

    instruction = instructions[i].split(' ')

    direction = 1 if instruction[1][0] == '+' else -1
    offset = int(instruction[1][1:])

    # Two branches: no change, change (nop -> jmp OR jmp -> nop)
    if instruction[0] == 'acc':
        return instruction_branch(instructions, visited, i + 1, accumulator + direction * offset, changed)
    elif changed:  # If previously changed, can't make another change
        if instruction[0] == 'jmp':
            return instruction_branch(instructions, visited, i + direction * offset, accumulator, changed)
        else:  # instruction[0] == 'nop'
            return instruction_branch(instructions, visited, i + 1, accumulator, changed)
    else:  # change is False
        # Try keeping instruction same and swapped operation
        if instruction[0] == 'jmp':
            branch_no_change = instruction_branch(instructions, visited, i + direction * offset, accumulator, False)
            branch_change = instruction_branch(instructions, visited, i + 1, accumulator, True)
        else:
            branch_no_change = instruction_branch(instructions, visited, i + 1, accumulator, False)
            branch_change = instruction_branch(instructions, visited, i + direction * offset, accumulator, True)

        # Evaluate branches to find best
        if branch_no_change is None and branch_change is None:
            return None
        elif branch_no_change is not None and branch_change is None:
            return branch_no_change
        elif branch_no_change is None and branch_change is not None:
            return branch_change
        else:
            return branch_no_change


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print(f'D8P1: {solve_part1("input.txt")}')
    print(f'D8P2: {solve_part2("input.txt")}')
