""" ADVENT OF CODE 2020 - DAY 4 - RAYMOND LI """

from __future__ import annotations

import re
from typing import Dict, List

REQUIRED_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
EYE_COLOURS = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def read_input(filepath: str) -> List[Dict[str, str]]:
    """Return processed version of the puzzle input.
    """
    with open(filepath) as input_file:
        passports = input_file.read().strip().split('\n\n')

    passport_fields = []
    passport_fields_split = []
    passport_fields_dict = []
    for passport in passports:
        # Split fields for each passport
        passport_fields.append(passport.replace('\n', ' ').split(' '))

        # Split keys/values for each passport
        passport_fields_split.append([fields.split(':') for fields in passport_fields[-1]])

        # Create dict of this passport's fields
        passport_fields_dict.append({k: v for k, v in passport_fields_split[-1]})

    return passport_fields_dict


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 4 Part 1 problem.
    """
    passports = read_input(filepath)

    valid = 0
    for i in range(len(passports)):
        # Check validity
        if all(field in passports[i] for field in REQUIRED_FIELDS):
            valid += 1

    return valid


def solve_part2(filepath: str) -> int:
    """Returns solution to Day 4 Part 2 problem.
    """
    passports = read_input(filepath)
    valid = 0
    for i in range(len(passports)):
        # Check validity
        if valid_passport(passports[i]):
            valid += 1

    return valid


def valid_passport(passport: Dict[str, str]) -> bool:
    """Return whether this passport is valid.

    Valid Passport Requirements (function returns True if all of these are true)
    - byr (Birth Year) - four digits; at least 1920 and at most 2002.
    - iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    - eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    - hgt (Height) - a number followed by either cm or in:
        - If cm, the number must be at least 150 and at most 193.
        - If in, the number must be at least 59 and at most 76.
    - hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    - ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    - pid (Passport ID) - a nine-digit number, including leading zeroes.
    - cid (Country ID) - ignored, missing or not.
    """

    # Check for all needed fields present
    all_required_fields = all(field in passport for field in REQUIRED_FIELDS)
    if not all_required_fields:
        return False

    # Check birth year
    if not (1920 <= int(passport['byr']) <= 2002):
        return False

    # Check issue year
    if not (2010 <= int(passport['iyr']) <= 2020):
        return False

    # Check expiration year
    if not (2020 <= int(passport['eyr']) <= 2030):
        return False

    # Check height
    if not passport['hgt'].endswith(('cm', 'in')):
        return False
    elif passport['hgt'].endswith('cm') and not (150 <= int(passport['hgt'][:-2]) <= 193):
        return False
    elif passport['hgt'].endswith('in') and not (59 <= int(passport['hgt'][:-2]) <= 76):
        return False

    # Check hair color
    if not passport['hcl'].startswith('#'):
        return False
    elif not re.match(r'#([a-f]|[0-9]){6}', passport['hcl']):
        return False

    # Check eye color
    if passport['ecl'] not in EYE_COLOURS:
        return False

    # Check passport id
    if not (len(passport['pid']) == 9 and passport['pid'].isdigit()):
        return False

    return True


if __name__ == '__main__':
    print(f'D4P1: {solve_part1("input.txt")}')
    print(f'D4P2: {solve_part2("input.txt")}')
