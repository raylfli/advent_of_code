"""
Advent of Code - Day 24: Crossed Wires
"""


def _parse_input_wires(s: str) -> dict[str, bool]:
    """
    Parse input wires into their initial values.
    """
    wires = {}
    for line in s.strip().split("\n"):
        wire, value = line.strip().split(": ")
        wires[wire] = value == "1"
    return wires


def _parse_input(
    s: str,
) -> tuple[
    dict[str, bool],
    set[str],
    dict[str, set[str]],
    dict[str, tuple[str, str, str]],
]:
    """
    Parse the input into a graph representation consisting of:
    1. input wire states
    2. all wires
    3. mapping of wire to outgoing connections
    4. mapping of an output wire to (left, operation, right) inputs
    """
    input_wires_str, gates_str = s.strip().split("\n\n")

    input_wires = _parse_input_wires(input_wires_str)

    vertices: set[str] = set()
    outgoing: dict[str, set[str]] = dict()
    operations: dict[str, tuple[str, str, str]] = dict()

    for line in gates_str.strip().split("\n"):
        input_str, out = line.strip().split(" -> ", maxsplit=1)
        left, op, right = input_str.strip().split(" ", maxsplit=2)

        for v in [left, right, out]:
            vertices.add(v)
            if v not in outgoing:
                outgoing[v] = set()
            operations[out] = left, op, right

        outgoing[left].add(out)
        outgoing[right].add(out)

    return input_wires, vertices, outgoing, operations


def _topological_sort(input_wires, outgoing, operations) -> list[str]:
    """
    Topologically sort the graph and return the ordering.
    """
    topo_l: list[str] = []
    resolved: set[str] = set()
    no_inc: set[str] = set(input_wires.keys())
    while len(no_inc) > 0:
        check = no_inc.pop()
        topo_l.append(check)
        resolved.add(check)

        for out in outgoing[check]:
            left, _, right = operations[out]
            if left in resolved and right in resolved:
                no_inc.add(out)

    return topo_l


def solve_part1(s: str) -> int:
    """
    Solve AoC D24 P1.
    """
    input_wires, _, outgoing, operations = _parse_input(s)

    # figure out what order to resolve the gates
    resolution_order = _topological_sort(input_wires, outgoing, operations)

    # now resolve all DAG nodes (i.e. the gates)
    wire_states = input_wires  # will mutate input_wires
    for out in resolution_order:
        if out not in operations:
            # must be an input wire
            continue

        left, op, right = operations[out]
        left_state = wire_states[left]
        right_state = wire_states[right]
        if op == "AND":
            gate_output = left_state and right_state
        elif op == "OR":
            gate_output = left_state or right_state
        elif op == "XOR":
            gate_output = left_state ^ right_state
        else:
            raise ValueError("Unsupported operation")
        wire_states[out] = gate_output

    # get output wires
    output_wires = [
        (wire, "1" if state else "0")
        for wire, state in wire_states.items()
        if wire[0] == "z"
    ]
    output_wires.sort(reverse=True)
    output_bin = "".join(state for _, state in output_wires)

    return int(output_bin, base=2)


def solve_part2(s: str) -> str:
    """
    Solve AoC D24 P2.
    """
    input_wires, _, _, operations = _parse_input(s)

    # the number of input bits of either x or y must be one less than the number of bits in z
    highest_z_bit = f"z{len(input_wires) // 2:02}"  # zero padded to two places

    # check operations for a bunch of rules -- we're working with a bunch of half/full adders
    # we care about figuring out which gates of the adders are wrong, but don't care about
    # actually swapping them
    swaps: set[str] = set()  # wrong label/gates
    for out, (left, op, right) in operations.items():
        # output bits must be an XOR gate
        # exception: highest z bit is a carry out
        if out[0] == "z" and op != "XOR" and out != highest_z_bit:
            swaps.add(out)

        # XOR gates must either output or directly process inputs
        elif op == "XOR" and all(
            c not in {"x", "y", "z"} for c in [left[0], right[0], out[0]]
        ):
            swaps.add(out)

        # XOR gates must feed to AND/XOR gates
        elif op == "XOR":
            for left1, op1, right1 in operations.values():
                if (out == left1 or out == right1) and op1 == "OR":
                    swaps.add(out)

        # AND gates must feed OR gates (except lowest bit)
        elif op == "AND" and left != "x00" and right != "x00":
            for left1, op1, right1 in operations.values():
                if (out == left1 or out == right1) and op1 != "OR":
                    swaps.add(out)

    swaps_lst = list(swaps)
    swaps_lst.sort()
    return ",".join(swaps_lst)
