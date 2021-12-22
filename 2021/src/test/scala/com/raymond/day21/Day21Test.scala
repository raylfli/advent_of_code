package com.raymond.day21

import org.scalatest.funsuite.AnyFunSuite

class Day21Test extends AnyFunSuite {

  val puzzleInput = "Player 1 starting position: 4\nPlayer 2 starting position: 8"

  test("Day21.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day21.solve1(input) == 739785)
  }

  test("Day21.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day21.solve2(input) == 444356092776315L)
  }

}
