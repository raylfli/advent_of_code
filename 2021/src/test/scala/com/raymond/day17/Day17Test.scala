package com.raymond.day17

import org.scalatest.funsuite.AnyFunSuite

class Day17Test extends AnyFunSuite {

  val puzzleInput = "target area: x=20..30, y=-10..-5"

  test("Day17.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day17.solve1(input) == 45)
  }

  test("Day17.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day17.solve2(input) == 112)
  }

}
