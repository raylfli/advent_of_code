"""
Advent of Code 2024 - Main script

https://adventofcode.com/2024
"""

import argparse
import os

from runner import Runner


if __name__ == '__main__':
    # create parser
    parser = argparse.ArgumentParser(
        prog='AoC 2024',
        description='Advent of Code 2024 - Python Solution'
    )
    parser.add_argument('day', help='Puzzle solution to run.')
    parser.add_argument('part', help='Puzzle solution part to run')
    parser.add_argument('-i', '--input', dest='input', help='Input file.', default=None)
    args = parser.parse_args()

    # process arguments
    day = int(args.day)
    part = int(args.part)
    raw_input_path = args.input
    if raw_input_path is None:
        raw_input_path = f'./inputs/d{day:02d}.txt'
    input_path = os.path.abspath(raw_input_path)

    # run solution
    r = Runner(day, part, input_path)
    solution = r.solve()

    print(f'--- Day {day} Part {part} Solution: {solution} ---')
