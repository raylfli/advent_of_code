package com.raymond.day9

import org.scalatest.funsuite.AnyFunSuite

class Day9Test extends AnyFunSuite {

  val puzzleInput = "2199943210\n3987894921\n9856789892\n8767896789\n9899965678"

  test("Day9.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day9.solve1(input) == 15)
  }

  test("Day9.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day9.solve2(input) == 1134)
  }

}
