package com.raymond.day5

import org.scalatest.funsuite.AnyFunSuite

class Day5Test extends AnyFunSuite {

  val puzzleInput = "0,9 -> 5,9\n8,0 -> 0,8\n9,4 -> 3,4\n2,2 -> 2,1\n7,0 -> 7,4\n6,4 -> 2,0\n0,9 -> 2,9\n3,4 -> 1,4\n0,0 -> 8,8\n5,5 -> 8,2"

  test("Day5.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day5.solve1(input) == 5)
  }

  test("Day5.processVentLine") {
    var input = "1,1 -> 1,3"
    assert(Day5.processVentLine(input).toVector == Vector((1,1), (1,2), (1,3)))

    input = "9,7 -> 7,7"
    assert(Day5.processVentLine(input).toVector == Vector((9,7), (8,7), (7,7)))
  }

  test("Day5.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day5.solve2(input) == 12)
  }

  test("Day5.processVentLineDiag") {
    var input = "1,1 -> 3,3"
    assert(Day5.processVentLineDiag(input).toVector == Vector((1,1), (2,2), (3,3)))

    input = "9,7 -> 7,9"
    assert(Day5.processVentLineDiag(input).toVector == Vector((9,7), (8,8), (7,9)))
  }

}
