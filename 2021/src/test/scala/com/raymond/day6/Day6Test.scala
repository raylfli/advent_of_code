package com.raymond.day6

import org.scalatest.funsuite.AnyFunSuite

class Day6Test extends AnyFunSuite {

  val puzzleInput = "3,4,3,1,2"

  test("Day6.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day6.solve1(input) == 5934)
  }

  test("Day6.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day6.solve2(input) == 26984457539L)
  }

}
