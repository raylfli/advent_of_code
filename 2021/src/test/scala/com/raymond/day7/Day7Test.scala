package com.raymond.day7

import org.scalatest.funsuite.AnyFunSuite

class Day7Test extends AnyFunSuite {

  val puzzleInput = "16,1,2,0,4,2,7,1,2,14"

  test("Day7.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day7.solve1(input) == 37)
  }

  test("Day7.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day7.solve2(input) == 168)
  }

}
