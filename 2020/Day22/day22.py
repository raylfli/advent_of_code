""" ADVENT OF CODE 2020 - DAY 22 - RAYMOND LI """

from __future__ import annotations

import logging
import queue
from typing import Tuple


def read_input(filepath: str) -> Tuple[queue.Queue, queue.Queue]:
    """Return processed version of the puzzle input.

    Returned tuple is in the format of: (player one card queue, player two card queue)
    """
    with open(filepath) as input_file:
        players = input_file.read().strip().split('\n\n')

    for i in range(len(players)):
        players[i] = players[i].split('\n')

    player_one = queue.Queue()
    player_two = queue.Queue()
    for card in range(1, len(players[0])):
        player_one.put(int(players[0][card]))
    for card in range(1, len(players[1])):
        player_two.put(int(players[1][card]))

    return player_one, player_two


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 22 Part 1 problem.

    >>> solve_part1('test1.txt')
    306
    """
    logging.debug(f'EXECUTING SOLVE - 1')
    player_one, player_two = read_input(filepath)

    while player_one.qsize() != 0 and player_two.qsize() != 0:
        do_turn(player_one, player_two)

    if player_one.qsize() > 0:
        return sum(player_one.get() * i for i in range(player_one.qsize(), 0, -1))
    elif player_two.qsize() > 0:
        return sum(player_two.get() * i for i in range(player_two.qsize(), 0, -1))


def do_turn(one: queue.Queue, two: queue.Queue) -> None:
    """Complete one turn of Combat.
    """
    one_card = one.get()
    two_card = two.get()
    if one_card > two_card:
        one.put(one_card)
        one.put(two_card)
    elif one_card < two_card:
        two.put(two_card)
        two.put(one_card)
    else:
        logging.warning(f'Combat tie happened! 1:{one_card} and 2:{two_card}')


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 22 Part 2 problem.

    >>> solve_part2('test1.txt')
    291
    """
    logging.debug(f'EXECUTING SOLVE - 2')
    player_one, player_two = read_input(filepath)

    winner = recursive_combat(player_one, player_two)

    if winner == 1:
        return sum(player_one.get() * i for i in range(player_one.qsize(), 0, -1))
    elif winner == 2:
        return sum(player_two.get() * i for i in range(player_two.qsize(), 0, -1))


def recursive_combat(one: queue.Queue, two: queue.Queue) -> int:
    """Complete a game of Recursive Combat.

    Returns 1 if player one wins, 2 if player 2 wins.
    """
    previous_rounds = set()
    while one.qsize() > 0 and two.qsize() > 0:
        if (tuple(one.queue), tuple(two.queue)) in previous_rounds:
            return 1
        previous_rounds.add((tuple(one.queue), tuple(two.queue)))
        one_card = one.get()
        two_card = two.get()
        if one.qsize() >= one_card and two.qsize() >= two_card:
            new_one, new_two = get_sub_deck(one_card, two_card, one, two)
            winner = recursive_combat(new_one, new_two)
            if winner == 1:
                one.put(one_card)
                one.put(two_card)
            elif winner == 2:
                two.put(two_card)
                two.put(one_card)
        else:
            if one_card > two_card:
                one.put(one_card)
                one.put(two_card)
            elif one_card < two_card:
                two.put(two_card)
                two.put(one_card)
    if one.qsize() == 0:
        return 2
    elif two.qsize() == 0:
        return 1
    else:
        logging.warning(f'Invalid q sizes: 1: {one.qsize()} -- 2: {two.qsize()}')


def get_sub_deck(one_num: int, two_num: int,
                 one_cards: queue.Queue, two_cards: queue.Queue) -> (queue.Queue, queue.Queue):
    """Returns the sub-decks containing the given number of cards for each player.

    Returned tuple is of the format: (player 1 cards, player 2 cards)
    """
    new_one_cards = queue.Queue()
    new_two_cards = queue.Queue()
    for n in range(one_num):
        new_one_cards.put(one_cards.queue[n])
    for n in range(two_num):
        new_two_cards.put(two_cards.queue[n])

    return (new_one_cards, new_two_cards)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D22P1: {solve_part1("input.txt")}')
    print(f'D22P2: {solve_part2("input.txt")}')
