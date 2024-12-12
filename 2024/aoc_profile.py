"""
Advent of Code 2024 - Profiler Class
"""

import cProfile

from solutions.d11 import solve_part2

if __name__ == '__main__':
    cProfile.run('solve_part2("125 17")')
