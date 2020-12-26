""" ADVENT OF CODE 2020 - DAY 14 - RAYMOND LI """

from __future__ import annotations

import logging
from typing import Dict, List, Set


def read_input(filepath: str) -> List[str]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        return input_file.read().strip().split('\n')


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 14 Part 1 problem.

    >>> solve_part1('test1.txt')
    165
    """
    instructions = read_input(filepath)

    memory = {}  # Dict[int, int]
    mask = ''
    for instruction in instructions:
        equals_sign_ind = instruction.find('=', 3)
        if instruction.startswith('mask'):
            mask = instruction[equals_sign_ind + 2:]
        elif instruction.startswith('mem'):
            loc = instruction[4:equals_sign_ind - 2]
            value = int(instruction[equals_sign_ind + 2:])
            memory[loc] = mask_value(mask, value)
        else:
            logging.warning(f"Invalid instruction: '{instruction}'")

    return sum(memory[loc] for loc in memory)


def mask_value(mask: str, value: int) -> int:
    """Returns the masked value.

    >>> mask_value('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 11)
    73
    >>> mask_value('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 101)
    101
    >>> mask_value('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 0)
    64
    """
    binary_str = bin(value)[2:]
    value_begin_ind = len(mask) - len(binary_str)
    new_binary_str = []
    for i in range(len(mask)):
        if i >= value_begin_ind:
            if mask[i] == 'X':
                new_binary_str.append(binary_str[i - value_begin_ind])
            else:
                new_binary_str.append(mask[i])
        else:
            if mask[i] == 'X':
                new_binary_str.append('0')
            else:
                new_binary_str.append(mask[i])

    return int(''.join(new_binary_str), 2)


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 14 Part 2 problem.

    >>> solve_part2('test2.txt')
    208
    """
    instructions = read_input(filepath)

    memory = {}  # Dict[int, int]
    mask = ''
    for instruction in instructions:
        equals_sign_ind = instruction.find('=', 3)
        if instruction.startswith('mask'):
            mask = instruction[equals_sign_ind + 2:]
        elif instruction.startswith('mem'):
            loc = instruction[4:equals_sign_ind - 2]
            value = int(instruction[equals_sign_ind + 2:])
            mask_value_with_float(memory, mask, loc, value)
        else:
            logging.warning(f"Invalid instruction: '{instruction}'")
        logging.debug(f'memory: {memory}')

    return sum(memory[loc] for loc in memory)


def mask_value_with_float(memory: Dict[int, int], mask: str, loc: str, value: int) -> None:
    """Mutates the memory with the problem required tasks.
    """
    binary_str = bin(int(loc))[2:]
    value_begin_ind = len(mask) - len(binary_str)
    new_memory_with_float = []
    for i in range(len(mask)):
        if i >= value_begin_ind:
            if mask[i] == 'X':
                new_memory_with_float.append('X')  # binary_str[i - value_begin_ind])
            elif mask[i] == '0':
                new_memory_with_float.append(binary_str[i - value_begin_ind])
            elif mask[i] == '1':
                new_memory_with_float.append('1')
            else:
                logging.warning(f'Invalid bitmask @ i={i}: {mask}')
        else:
            if mask[i] == 'X':
                new_memory_with_float.append('X')
            else:
                new_memory_with_float.append(mask[i])

    memory_locs_to_change = set()  # Set[int]
    recursive_generate_memory(memory_locs_to_change, ''.join(new_memory_with_float))
    logging.debug(f'memory_locs_to_change: {memory_locs_to_change}')

    for loc in memory_locs_to_change:
        memory[loc] = value


def recursive_generate_memory(s: Set[int], floating_memory: str, start_ind: int = 0) -> None:
    """Mutates provided set to have all the generated memory locations.
    """
    x_ind = floating_memory.find('X', start_ind)
    if x_ind == -1:
        s.add(int(floating_memory, 2))
    else:
        recursive_generate_memory(s, f'{floating_memory[:x_ind]}1{floating_memory[x_ind + 1:]}', x_ind)
        recursive_generate_memory(s, f'{floating_memory[:x_ind]}0{floating_memory[x_ind + 1:]}', x_ind)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D14P1: {solve_part1("input.txt")}')
    print(f'D14P2: {solve_part2("input.txt")}')
