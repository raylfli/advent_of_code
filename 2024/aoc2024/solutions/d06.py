"""
Advent of Code - Day 6: Guard Gallivant
"""


def _parse_lab(s: str) -> (list[str], (int, int)):
    """
    Parse the lab into rows and return the starting location of the guard.
    """
    rows = []
    guard = (-1, -1)
    for r, row in enumerate(s.strip().split("\n")):
        rows.append(row.strip())
        for c, cell in enumerate(rows[-1]):
            if cell == "^":
                guard = (r, c)
    return rows, guard


def _check_obstacle(rows: list[str], r: int, c: int) -> bool:
    """
    Check if the given cell is an obstacle.

    Returns True IFF the cell is an obstacle. Boundaries are NOT considered as obstacles.
    """
    if 0 <= r < len(rows) and 0 <= c < len(rows[0]):
        return rows[r][c] == "#"

    return False


def _traverse(
    rows: list[str], start_r: int, start_c: int, dr: int = -1, dc: int = 0
) -> set[(int, int, int, int)]:
    """
    Traverse the lab going upwards from (start_r, start_c) until exiting it.

    Return the cells visited, raises ValueError if a loop is encountered.
    """
    r, c = start_r, start_c
    visited = set()
    while 0 <= r < len(rows) and 0 <= c < len(rows[0]):
        visited.add((r, c))

        # check if obstacle in front
        if _check_obstacle(rows, r + dr, c + dc):
            dr, dc = dc, dr * -1

        # move
        r, c = r + dr, c + dc

    return visited


def _check_loop(
    rows: list[str], start_r: int, start_c: int, dr: int = -1, dc: int = 0
) -> bool:
    """
    Check whether a loop is present with this traversal.
    """
    r, c = start_r, start_c
    visited = set()
    while 0 <= r < len(rows) and 0 <= c < len(rows[0]):
        if (r, c, dr, dc) in visited:
            return True
        visited.add((r, c, dr, dc))

        # check if obstacle in front
        if _check_obstacle(rows, r + dr, c + dc):
            dr, dc = dc, dr * -1

        # move
        else:
            r, c = r + dr, c + dc

    return False


def _traverse_obstacle_count(rows: list[str], r: int, c: int) -> int:
    """
    Count the number of obstacles that can be introduced to introduce a loop.
    """
    blocks = set()  # set[(int, int)]
    visited = set()  # set[(int, int)]

    start_r, start_c = r, c
    dr, dc = -1, 0

    while 0 <= r < len(rows) and 0 <= c < len(rows[0]):
        visited.add((r, c))

        new_r, new_c = r + dr, c + dc
        if _check_obstacle(rows, new_r, new_c):
            # obstacle in front can only turn
            dr, dc = dc, dr * -1
        else:
            if (
                0 <= new_r < len(rows)
                and 0 <= new_c < len(rows[0])
                and (new_r, new_c) != (start_r, start_c)
                and (new_r, new_c) not in visited
            ):
                # try placing a block in front
                new_rows = rows.copy()
                new_rows[new_r] = (
                    new_rows[new_r][:new_c] + "#" + new_rows[new_r][new_c + 1 :]
                )
                if _check_loop(new_rows, r, c, dc, dr * -1):
                    blocks.add((new_r, new_c))
            r, c = new_r, new_c

    return len(blocks)


def solve_part1(s: str) -> int:
    """
    Solve AoC D6 P1.
    """
    rows, (start_r, start_c) = _parse_lab(s)
    visited = _traverse(rows, start_r, start_c)
    return len(visited)


def solve_part2(s: str) -> int:
    """
    Solve AoC D6 P2.
    """
    rows, (start_r, start_c) = _parse_lab(s)
    return _traverse_obstacle_count(rows, start_r, start_c)
