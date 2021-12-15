package com.raymond.day15

import org.scalatest.funsuite.AnyFunSuite

class Day15Test extends AnyFunSuite {

  val puzzleInput = "1163751742\n1381373672\n2136511328\n3694931569\n7463417111\n1319128137\n1359912421\n3125421639\n1293138521\n2311944581"

  test("Day15.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day15.solve1(input) == 40)
  }

  test("Day15.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day15.solve2(input) == 315)
  }

}
