"""
Advent of Code - Day 15: Warehouse Woes
"""

type Grid = list[list[str]]
type GridIndex = tuple[int, int]
type Direction = tuple[int, int]


def _parse_grid(s: str) -> tuple[Grid, GridIndex]:
    """
    Parse the grid into a 2D list representation modifying grid positions if needed.

    2D list chosen over 1D list of strings to allow for modification later.

    Returns the grid's 2D list representation and the robot's location.
    """
    grid = []
    robot_loc = (-1, -1)
    for r, row in enumerate(s.strip().split('\n')):
        grid.append([])
        for c, cell in enumerate(row.strip()):
            if cell == '@':
                robot_loc = (r, c)
                grid[-1].append('.')  # no need to represent robot, will track coordinates
            else:
                grid[-1].append(cell)

    return grid, robot_loc


def _parse_grid_double_set(s: str) -> tuple[set[GridIndex], set[GridIndex], GridIndex]:
    """
    Parse the grid into a double sized version representing boxes and walls as sets.

    Returns the box locations (left cell of the box), wall locations, and the robot's location.
    """
    s = s.translate({
        ord('#'): '##',
        ord('O'): '[]',
        ord('.'): '..',
        ord('@'): '@.'
    })
    boxes: set[GridIndex] = set()
    walls: set[GridIndex] = set()
    robot_loc = (-1, -1)
    for r, row in enumerate(s.strip().split('\n')):
        for c, cell in enumerate(row.strip()):
            if cell == '@':
                robot_loc = (r, c)
            elif cell == '#':
                walls.add((r, c))
            elif cell == '[':
                boxes.add((r, c))
    return boxes, walls, robot_loc


def _parse_moves(s: str) -> list[Direction]:
    """
    Parse the list of moves into a list of directions.
    """
    moves = []
    for c in s.strip():
        match c:
            case '<':
                moves.append((0, -1))
            case '>':
                moves.append((0, 1))
            case '^':
                moves.append((-1, 0))
            case 'v':
                moves.append((1, 0))
            case _:
                pass
    return moves


def _parse_input(s: str, double_size: bool = False) -> tuple[Grid, GridIndex, list[Direction]]:
    """
    Parse the input string into a warehouse map and a list of moves.
    """
    map_str, dirs_str = s.strip().split('\n\n', maxsplit=1)
    if double_size:
        map_str = map_str.translate({
            ord('#'): '##',
            ord('O'): '[]',
            ord('.'): '..',
            ord('@'): '@.'
        })
    grid, robot = _parse_grid(map_str)
    moves = _parse_moves(dirs_str)
    return grid, robot, moves


def _check_box_push(grid: Grid, loc: GridIndex, d: Direction) -> GridIndex | None:
    """
    Return the grid index of an empty space that a box should be pushed into from
    the robot's location `loc`.

    Returns None if conditions are not met for a box ot be pushed.
    """
    r, c = loc
    dr, dc = d
    max_r, max_c = len(grid) - 1, len(grid[0]) - 1

    blank_space = None
    while 0 <= r <= max_r and 0 <= c <= max_c:
        r, c = r + dr, c + dc  # first iteration is guaranteed OK, robot will never be on the edge
        if grid[r][c] == '#':
            break  # exit loop, can't push box anywhere
        elif grid[r][c] == '.':
            blank_space = (r, c)
            break  # exit loop, found blank space

        # otherwise, we found a box -> continue checking for empty spaces

    return blank_space


def _check_box_push_vert_double(grid: Grid, loc: GridIndex, d: Direction) -> set[GridIndex] | None:
    """
    Return a set of valid cells that can be pushed.

    Returns None if conditions are not met for a box to be pushed.
    """
    r, c = loc
    dr, dc = d
    check_r, check_c = r + dr, c + dc
    check_cell = grid[check_r][check_c]

    # base cases
    if check_cell == '.':
        return {loc}
    elif check_cell == '#':
        return None

    # otherwise, need to check if a different box can be pushed
    to_check = []
    if check_cell == '[':
        to_check.append((check_r, check_c))
        to_check.append((check_r, check_c + 1))
    else:
        to_check.append((check_r, check_c - 1))
        to_check.append((check_r, check_c))

    checks = [_check_box_push_vert_double(grid, gi, d) for gi in to_check]
    push_cells: set[GridIndex] = set()
    if any(check is None for check in checks):
        return None
    else:
        for check in checks:
            push_cells = push_cells | check
        return push_cells | {loc}


def _calculate_gps(grid: Grid) -> int:
    """
    Sum all the GPS coordinates of all the boxes.
    """
    total = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'O' or cell == '[':
                total += r * 100 + c
    return total


def solve_part1(s: str) -> int:
    """
    Solve AoC D15 P1.
    """
    grid, robot_loc, moves = _parse_input(s)
    r, c = robot_loc
    for d in moves:
        dr, dc = d
        box_loc = _check_box_push(grid, (r, c), d)
        if box_loc is not None:
            # move box
            br, bc = box_loc
            grid[br][bc] = 'O'

            # move robot and reset box
            # if no box to be moved, this will overwrite the newly created box
            r, c = r + dr, c + dc
            grid[r][c] = '.'

    return _calculate_gps(grid)


def _str_grid(grid: Grid, robot_loc: GridIndex) -> str:
    """
    Stringify grid and robot position.
    """
    lst = []
    for r, row in enumerate(grid):
        lst2 = []
        for c, cell in enumerate(row):
            if (r, c) == robot_loc:
                lst2.append('@')
            else:
                lst2.append(cell)
        lst.append(''.join(lst2))
    return '\n'.join(lst)


def solve_part2(s: str) -> int:
    """
    Solve AoC D15 P2.
    """
    grid, robot_loc, moves = _parse_input(s, double_size=True)
    r, c = robot_loc
    for d in moves:
        dr, dc = d
        check_r, check_c = r + dr, c + dc
        check_cell = grid[check_r][check_c]

        # check for only robot move
        if check_cell == '.':
            r, c = check_r, check_c
            continue
        elif check_cell == '#':
            continue  # hit a wall

        # check for movement in sideways direction
        if dr == 0:
            space_loc = _check_box_push(grid, (r, c), d)
            if space_loc is not None:
                if dc == -1:  # moving left
                    new_left = space_loc[1]
                    new_right = c - 1
                    left = space_loc[1] + 1
                    right = c
                else:  # moving right
                    new_left = c + 2
                    new_right = space_loc[1] + 1
                    left = c + 1
                    right = space_loc[1]
                grid[r][new_left:new_right] = grid[r][left:right]

                # move robot
                r, c = r + dr, c + dc
                grid[r][c] = '.'
            continue

        # box must be being pushed up or down

        # check if that box can move
        # - this means both cells of the box can move
        if check_cell == '[':
            push_box_l = check_r - dr, check_c
            push_box_r = check_r - dr, check_c + 1
        else:
            push_box_l = check_r - dr, check_c - 1
            push_box_r = check_r - dr, check_c

        check_box_l = _check_box_push_vert_double(grid, push_box_l, d)
        check_box_r = _check_box_push_vert_double(grid, push_box_r, d)

        if check_box_l is None or check_box_r is None:
            continue  # no boxes can move
        else:
            # move the boxes
            cells_to_move = check_box_l | check_box_r
            cells_to_move -= {push_box_l}
            cells_to_move -= {push_box_r}
            cells_to_move |= {(check_r, check_c)}
            to_move = list(cells_to_move)
            to_move.sort(reverse=dr == 1)  # sort to guarantee order of movement

            for r1, c1 in to_move:
                r2, c2 = r1 + dr, c1 + dc
                grid[r2][c2] = grid[r1][c1]
                grid[r1][c1] = '.'

            # move the robot
            r, c = r + dr, c + dc

    return _calculate_gps(grid)
