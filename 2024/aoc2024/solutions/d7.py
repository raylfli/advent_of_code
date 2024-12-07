"""
Advent of Code - Day 7: Bridge Repair
"""


def _parse_equation(s: str) -> tuple[int, tuple[int, ...]]:
    """
    Parse single equation to the target number and a tuple of numbers.
    """
    target, raw_nums = s.split(': ', maxsplit=1)
    target = int(target)
    nums = tuple(int(n) for n in raw_nums.strip().split(' '))
    return target, nums


def check_equation(target: int, nums: tuple[int, ...], concat: bool = False) -> bool:
    """
    Return whether this equation could be true.

    Available operators are addition or multiplication.
    """
    # check if target number achieved
    if len(nums) == 1:
        return target == nums[0]

    a, b, *rest = nums

    num_add = a + b
    num_mul = a * b
    num_concat = a * (10 ** len(str(b))) + b

    # no need to process more, already overshot
    if num_add > target and num_mul > target and (not concat or num_concat > target):
        return False

    res_add = check_equation(target, (num_add, *rest), concat=concat)
    res_mul = check_equation(target, (num_mul, *rest), concat=concat)
    res_concat = True if not concat else check_equation(target, (num_concat, *rest), concat=concat)

    return res_add or res_mul or (concat and res_concat)


def solve_part1(s: str, concat: bool = False) -> int:
    """
    Solve AoC D7 P1.
    """
    total = 0
    for equation in s.strip().split('\n'):
        target, nums = _parse_equation(equation)
        if check_equation(target, nums, concat=concat):
            total += target
    return total


def solve_part2(s: str) -> int:
    """
    Solve AoC D7 P2.
    """
    return solve_part1(s, concat=True)
