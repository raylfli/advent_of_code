package com.raymond.day23

import org.scalatest.funsuite.AnyFunSuite

class Day23Test extends AnyFunSuite {

  val puzzleInput = "#############\n#...........#\n###B#C#B#D###\n  #A#D#C#A#\n  #########"

  test("Day23.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day23.solve1(input) == 12521)
  }

  test("Day23.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day23.solve2(input) == 44169)
  }

}
