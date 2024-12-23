"""
Advent of Code - Day 23: LAN Party
"""

from itertools import combinations


def _parse_input(s: str) -> tuple[dict[str, int], list[str], list[list[bool]]]:
    """
    Parse the input into a graph representation consisting of:
    1. a mapping from a computer to a numerical index
    2. a mapping of an index to a computer
    3. an adjacency matrix of computer connections
    """
    indices: dict[str, int] = {}
    labels: list[str] = []
    connections_raw: list[tuple[int, int]] = []
    for line in s.strip().split("\n"):
        left, right = line.strip().split("-", maxsplit=1)
        if left not in indices:
            indices[left] = len(labels)
            labels.append(left)
        if right not in indices:
            indices[right] = len(labels)
            labels.append(right)
        connections_raw.append((indices[left], indices[right]))

    # construct adjacency matrix
    adj: list[list[bool]] = []
    for _outer in range(len(labels)):
        adj.append([])
        for _inner in range(len(labels)):
            adj[-1].append(False)

    for left, right in connections_raw:
        adj[left][right] = True
        adj[right][left] = True

    return indices, labels, adj


def solve_part1(s: str) -> int:
    """
    Solve AoC D23 P1.

    This is a k-clique problem.
    """
    indices, labels, adj = _parse_input(s)

    # only interested in t-computers
    t_computers = {label: index for label, index in indices.items() if label[0] == "t"}
    t_indices = set(t_computers.values())

    total = 0
    for a, b, c in combinations(range(len(labels)), 3):
        if a in t_indices or b in t_indices or c in t_indices:
            if adj[a][b] and adj[b][c] and adj[a][c]:
                total += 1

    return total


def solve_part2(s: str) -> str:
    """
    Solve AoC D23 P2.

    This is a maximum clique problem.
    """
    _, labels, adj = _parse_input(s)

    # find all maximal cliques
    maximal_cliques: list[list[str]] = []
    for i, label_i in enumerate(labels):
        clique: set[int] = {i}
        clique_labels: list[str] = [label_i]
        for j, label_j in enumerate(labels):
            if i != j and all(adj[j][c] for c in clique):
                clique.add(j)
                clique_labels.append(label_j)
        maximal_cliques.append(clique_labels)

    # find all maximum clique
    clique_number = max(map(len, maximal_cliques))
    for maximal_clique in maximal_cliques:
        if len(maximal_clique) == clique_number:
            maximal_clique.sort()
            return ",".join(maximal_clique)

    return ""
