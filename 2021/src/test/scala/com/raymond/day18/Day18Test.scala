package com.raymond.day18

import org.scalatest.funsuite.AnyFunSuite

class Day18Test extends AnyFunSuite {

  val puzzleInput1 = "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]\n[[[5,[2,8]],4],[5,[[9,9],0]]]\n[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]\n[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]\n[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]\n[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]\n[[[[5,4],[7,7]],8],[[8,3],8]]\n[[9,3],[[9,9],[6,[4,9]]]]\n[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]\n[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"
  val puzzleInput2 = "[[[[4,3],4],4],[7,[[8,4],9]]]\n[1,1]"
  val puzzleInput3 = "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]\n[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]\n[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]\n[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]\n[7,[5,[[3,8],[1,4]]]]\n[[2,[2,2]],[8,[8,1]]]\n[2,9]\n[1,[[[9,3],9],[[9,0],[0,7]]]]\n[[[5,[7,4]],7],1]\n[[[[4,2],2],6],[8,7]]"


  test("Day18.constructTree_1") {
    val input = "2"
    val expected = new Number(2)

    assert(Day18.constructTree(input) == expected)
  }

  test("Day18.constructTree_2") {
    val input = "[5,6]"
    val expected = new Pair(new Number(5), new Number(6))

    assert(Day18.constructTree(input) == expected)
  }

  test("Day18.constructTree_3") {
    val input = "[1,[2,3]]"
    val expected = new Pair(new Number(1), new Pair(new Number(2), new Number(3)))

    assert(Day18.constructTree(input) == expected)
  }

  test("Day18.constructTree_4") {
    val input = "[[1,2],[3,4]]"
    val expected = new Pair(new Pair(new Number(1), new Number(2)), new Pair(new Number(3), new Number(4)))

    assert(Day18.constructTree(input) == expected)
  }

  test("Day18.split_1") {
    val input = new Number(1)
    val expected = new Number(1)

    assert(Day18.split(input) == (expected, false))
  }

  test("Day18.split_2") {
    val input = new Number(10)
    val expected = new Pair(new Number(5), new Number(5))

    assert(Day18.split(input) == (expected, true))
  }

  test("Day18.split_3") {
    val input = new Number(11)
    val expected = new Pair(new Number(5), new Number(6))

    assert(Day18.split(input) == (expected, true))
  }

  test("Day18.split_4") {
    val input = new Pair(new Number(1), new Number(2))
    val expected = new Pair(new Number(1), new Number(2))

    assert(Day18.split(input) == (expected, false))
  }

  test("Day18.split_5") {
    val input = new Pair(new Number(20), new Number(2))
    val expected = new Pair(new Pair(new Number(10), new Number(10)), new Number(2))

    assert(Day18.split(input) == (expected, true))
  }
  test("Day18.split_6") {
    val input = new Pair(new Number(21), new Number(2))
    val expected = new Pair(new Pair(new Number(10), new Number(11)), new Number(2))

    assert(Day18.split(input) == (expected, true))
  }

  test("Day18.explode_1") {
    val input = Day18.constructTree("[[[[[9,8],1],2],3],4]")
    val expected = Day18.constructTree("[[[[0,9],2],3],4]")

    assert(Day18.explode(input)(0) == expected)
  }

  test("Day18.explode_2") {
    val input = Day18.constructTree("[7,[6,[5,[4,[3,2]]]]]")
    val expected = Day18.constructTree("[7,[6,[5,[7,0]]]]")

    assert(Day18.explode(input)(0) == expected)
  }

  test("Day18.explode_3") {
    val input = Day18.constructTree("[[6,[5,[4,[3,2]]]],1]")
    val expected = Day18.constructTree("[[6,[5,[7,0]]],3]")

    assert(Day18.explode(input)(0) == expected)
  }

  test("Day18.explode_4") {
    val input = Day18.constructTree("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    val expected = Day18.constructTree("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")

    assert(Day18.explode(input)(0) == expected)
  }

  test("Day18.explode_5") {
    val input = Day18.constructTree("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    val expected = Day18.constructTree("[[3,[2,[8,0]]],[9,[5,[7,0]]]]")

    assert(Day18.explode(input)(0) == expected)
  }

  test("Day18.reduce_1") {
    val input = Day18.constructTree("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
    val expected = Day18.constructTree("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

    assert(Day18.reduce(input) == expected)
  }

  test("Day18.reduce_2") {
    val input = Day18.constructTree("[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]")
    val expected = Day18.constructTree("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]")

    assert(Day18.reduce(input) == expected)
  }

  test("Day18.reduce_3") {
    val input = Day18.constructTree("[[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]]")
    val expected = Day18.constructTree("[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]")

    assert(Day18.reduce(input) == expected)
  }

  test("Day18.reduce_4") {
    val input = Day18.constructTree("[[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]]")
    val expected = Day18.constructTree("[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]")

    assert(Day18.reduce(input) == expected)
  }

  test("Day18.solve1_1") {
    val input = puzzleInput1.split(raw"\n").iterator

    assert(Day18.solve1(input) == 4140)
  }

  test("Day18.solve1_2") {
    val input = puzzleInput3.split(raw"\n").iterator

    assert(Day18.solve1(input) == 3488)
  }

  test("Day18.solve2") {
    val input = puzzleInput1.split(raw"\n").iterator

    assert(Day18.solve2(input) == 3993)
  }

}
