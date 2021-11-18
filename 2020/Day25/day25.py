""" ADVENT OF CODE 2020 - DAY 25 - RAYMOND LI """

from __future__ import annotations

import logging


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 25 Part 1 problem.

    >>> solve_part1('test1.txt')
    14897079
    """
    logging.debug(f'EXECUTING SOLVE - 1')
    with open(filepath) as input_file:
        public_keys = input_file.read().strip().split('\n')
    card_public, door_public = public_keys

    base = 7
    mod = 20201227

    return crack_diffie_hellman_exchange(int(card_public), int(door_public), base, mod)


def crack_diffie_hellman_exchange(public_a: int, public_b: int, base_prime: int, mod: int) -> int:
    """Returns the cracked Diffie-Hellman private key.
    """
    for exp in range(1, mod):
        if pow(base_prime, exp, mod) == public_a:
            return pow(public_b, exp, mod)

    return -1


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D25P1: {solve_part1("input.txt")}')
    # No part 2, all 49 stars achieved! :)
    # 7973th person to finish all puzzles.
