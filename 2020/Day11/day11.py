""" ADVENT OF CODE 2020 - DAY 11 - RAYMOND LI """

from __future__ import annotations

from typing import List


def read_input(filepath: str) -> List[str]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        return input_file.read().strip().split('\n')


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 11 Part 1 problem.

    >>> solve_part1('test1.txt')
    37
    """
    rows = read_input(filepath)
    rows.insert(0, '.' * len(rows[0]))
    rows.append('.' * len(rows[0]))
    for i in range(0, len(rows)):
        rows[i] = '.' + rows[i] + '.'

    original_seating = rows
    while True:
        new_seating = original_seating.copy()
        for i in range(1, len(original_seating) - 1):
            new_string = ['.']
            for j in range(1, len(original_seating[i]) - 1):
                if original_seating[i][j] != '.':
                    new_string.append(check_around([row[j - 1: j + 2] for row in original_seating[i - 1: i + 2]]))
                else:
                    new_string.append('.')
            new_string.append('.')
            new_seating[i] = ''.join(new_string)

        if new_seating == original_seating:
            return sum(sum(seat == '#' for seat in row) for row in new_seating)
        else:
            original_seating = new_seating


def check_around(seats: List[str]) -> str:
    """Returns the new middle seat character.

    Preconditions:
        - len(seats) == 3
        - all(len(row) == 3 for row in seats)
    """
    if seats[1][1] == '#':  # occupied
        if sum(sum(seat == '#' for seat in row) for row in seats) - 1 >= 4:
            return 'L'
        else:
            return '#'

    elif seats[1][1] == 'L':  # empty
        if sum(sum(seat == '#' for seat in row) for row in seats) == 0:
            return '#'
        else:
            return 'L'

    else:
        return seats[1][1]


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 11 Part 2 problem.

    >>> solve_part2('test1.txt')
    26
    """
    rows = read_input(filepath)
    rows.insert(0, 'x' * len(rows[0]))
    rows.append('x' * len(rows[0]))
    for i in range(0, len(rows)):
        rows[i] = 'x' + rows[i] + 'x'

    original_seating = rows
    while True:
        new_seating = original_seating.copy()
        for i in range(1, len(original_seating) - 1):
            new_string = ['x']
            for j in range(1, len(original_seating[i]) - 1):
                if original_seating[i][j] != '.':
                    new_string.append(check_around_part2(original_seating, i, j))
                else:
                    new_string.append('.')
            new_string.append('x')
            new_seating[i] = ''.join(new_string)

        if new_seating == original_seating:
            return sum(sum(seat == '#' for seat in row) for row in new_seating)
        else:
            original_seating = new_seating


def check_around_part2(seats: List[str], row: int, col: int) -> str:
    """Returns the new middle seat character.

    Seats should be all the seats on the ferry.
    """
    DIRECTIONS = {'NW', 'N', 'NE', 'W', 'E', 'SW', 'S', 'SE'}
    # occupation = [first_visible_occupied(seats, direction, row, col) for direction in DIRECTIONS]
    if seats[row][col] == '#':  # occupied
        if sum([first_visible_occupied(seats, direction, row, col, True) for direction in DIRECTIONS]) >= 5:
            return 'L'
        else:
            return '#'

    elif seats[row][col] == 'L':  # empty
        if sum([first_visible_occupied(seats, direction, row, col, True) for direction in DIRECTIONS]) == 0:
            return '#'
        else:
            return 'L'

    else:
        return seats[row][col]


def first_visible_occupied(seats: List[str], direction: str, row: int, col: int, original: bool) -> bool:
    """Return whether the first visible seat is occupied.

    Original marks whether this current seat should be ignored.

    Possible directions ([.] marks the current seat):
        - [NW] [N] [NE]
        - [W]  [.] [E]
        - [SW] [S] [SE]

    Preconditions:
        - all(len(row) == len(row[0]) for row in seats)
        - 0 <= x <= len(seats[0]) - 1
        - 0 <= y <= len(seats) - 1
    """
    if not original:
        if seats[row][col] == 'x' or seats[row][col] == 'L':
            return False
        elif seats[row][col] == '#':
            return True

    if direction == 'NW':
        row -= 1
        col -= 1
    elif direction == 'N':
        row -= 1
    elif direction == 'NE':
        row -= 1
        col += 1
    elif direction == 'W':
        col -= 1
    elif direction == 'E':
        col += 1
    elif direction == 'SW':
        row += 1
        col -= 1
    elif direction == 'S':
        row += 1
    elif direction == 'SE':
        row += 1
        col += 1
    else:
        print('rip')

    return first_visible_occupied(seats, direction, row, col, False)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    print(f'D11P1: {solve_part1("input.txt")}')
    print(f'D11P2: {solve_part2("input.txt")}')
