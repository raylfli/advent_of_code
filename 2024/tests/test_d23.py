"""
Advent of Code 2024 - Day 23 Tests
"""

from solutions.d23 import solve_part1, solve_part2


class TestSuite:

    INPUT_STR_1 = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


class TestPart1(TestSuite):

    def test_1(self):
        assert solve_part1(self.INPUT_STR_1) == 7


class TestPart2(TestSuite):

    def test_1(self):
        assert solve_part2(self.INPUT_STR_1) == "co,de,ka,ta"
