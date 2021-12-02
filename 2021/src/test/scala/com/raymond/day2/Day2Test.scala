package com.raymond.day2

import org.scalatest.funsuite.AnyFunSuite

class Day2Test extends AnyFunSuite {

  val puzzleInput = "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2"

  test("Day2.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(150 == Day2.solve1(input))
  }

  test("Day2.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(900 == Day2.solve2(input))
  }

}
