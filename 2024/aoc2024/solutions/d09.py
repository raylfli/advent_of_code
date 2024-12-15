"""
Advent of Code - Day 9: Disk Fragmenter
"""


def _parse_disk(s: str) -> tuple[list[int], list[int]]:
    """
    Generate a list representation of the disk and a list of file lengths.
    """
    disk = []
    files = []
    file_flag = True
    for digit in s.strip():
        digit = int(digit)
        file_id = len(files)
        if file_flag:
            disk.extend([file_id] * digit)
            files.append(digit)
        else:
            disk.extend([-1] * digit)
        file_flag = not file_flag

    return disk, files


def _compute_checksum(disk: list[int]) -> int:
    """
    Compute the checksum of this disk.

    Note that -1s are treated as blank.
    """
    total = 0
    for i, file in enumerate(disk):
        if file != -1:
            total += i * file
    return total


def _find_first_blank(disk: list[int], size: int) -> int | None:
    """
    Find the index of the first blank of the given size or greater.

    Returns None if not found.
    """
    start_i = None
    for i in range(len(disk)):
        if disk[i] != -1:
            if start_i is not None and i - start_i >= size:
                return start_i
            start_i = None
        if start_i is None and disk[i] == -1:
            start_i = i

    return None


def _move_file(
    disk: list[int],
    file_id: int,
    file_size: int,
    file_location: int,
    blank_location: int,
):
    """
    Moves file at index file_location into index blank_location.
    """
    disk[blank_location : blank_location + file_size] = [file_id] * file_size
    disk[file_location : file_location + file_size] = [-1] * file_size


def solve_part1(s: str) -> int:
    """
    Solve AoC D9 P1.
    """
    disk, _ = _parse_disk(s)

    # disk compaction
    blank_i = 0
    file_i = len(disk) - 1

    # move blank pointer to first blank
    while disk[blank_i] != -1:
        blank_i += 1

    # move file pointer to last file block
    while disk[file_i] == -1:
        file_i -= 1

    while blank_i < file_i:
        # move file block
        disk[blank_i] = disk[file_i]
        disk[file_i] = -1

        # move blank pointer to next blank
        while disk[blank_i] != -1:
            blank_i += 1

        # move file pointer to next file
        while disk[file_i] == -1:
            file_i -= 1

    # compute checksum
    return _compute_checksum(disk)


def solve_part2(s: str) -> int:
    """
    Solve AoC D9 P2.
    """
    # unoptimized: super slow string processing
    # linked list perhaps better?
    disk, files = _parse_disk(s)
    for file_id, size in reversed(list(enumerate(files))):
        valid_blank_i = _find_first_blank(disk, size)
        file_i = disk.index(
            file_id
        )  # raises ValueError if not found, should never arise
        if valid_blank_i is not None and file_i >= valid_blank_i:
            _move_file(disk, file_id, size, file_i, valid_blank_i)

    # compute checksum
    return _compute_checksum(disk)
