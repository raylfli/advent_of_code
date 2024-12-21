"""
Advent of Code - Day 17: Chronospatial Computer
"""


def _parse_input(s: str) -> tuple[list[int], list[int]]:
    """
    Parse input string into a list of initial register values
    and a list of program instructions.
    """
    register_strs, program_str = s.strip().split("\n\n", maxsplit=1)

    registers = []
    for line in register_strs.strip().split("\n"):
        registers.append(int(line.split(": ", maxsplit=1)[1]))

    program = [int(n) for n in program_str.split(": ", maxsplit=1)[1].split(",")]

    return registers, program


def _run_program(registers: list[int], program: list[int]) -> list[int]:
    """
    Run the program on the given initial register values and program instructions.
    """
    ins_pt = 0
    outputs = []
    while ins_pt < len(program):
        opcode, combo = program[ins_pt], program[ins_pt + 1]

        # resolve combo
        if 4 <= combo <= 6:
            combo = registers[combo - 4]

        if opcode == 0:  # adv
            registers[0] = registers[0] >> combo
        elif opcode == 1:  # bxl
            registers[1] = registers[1] ^ combo
        elif opcode == 2:  # bst
            registers[1] = combo & 0b111
        elif opcode == 3:  # jnz
            if registers[0] != 0:
                ins_pt = combo
                continue  # jump directly!
        elif opcode == 4:  # bxc
            registers[1] = registers[1] ^ registers[2]
        elif opcode == 5:  # out
            outputs.append(combo & 0b111)
        elif opcode == 6:  # bdv
            registers[1] = registers[0] >> combo
        elif opcode == 7:  # cdv
            registers[2] = registers[0] >> combo

        ins_pt += 2
    return outputs


def _generate_program(program: list[int]) -> int:
    """
    Return the minimum starting register A value to replicate the program itself.
    """

    def _generate_program_recur(i: int, acc: int) -> int | None:
        """
        Recursively generate the program.
        """
        for n in range(8):
            reg_a = (acc << 3) + n
            if _run_program([reg_a, 0, 0], program) == program[i:]:
                if i == 0:
                    return reg_a
                ret = _generate_program_recur(i - 1, reg_a)
                if ret is not None:
                    return ret
        return None

    return _generate_program_recur(len(program) - 1, 0)


def solve_part1(s: str) -> str:
    """
    Solve AoC D17 P1.
    """
    registers, program = _parse_input(s)

    return ",".join(str(n) for n in _run_program(registers, program))


def solve_part2(s: str) -> int:
    """
    Solve AoC D17 P2.

    Each 'iteration' of my input program only depends on register A. B, and C are set
    by the value of A at the beginning of the iteration.

    Additionally, only the last 3 bits of A matter at any given iteration, so we only need to
    check candidates in the range of 0-7.
    """
    _, program = _parse_input(s)
    return _generate_program(program)
