package com.raymond.day11

import org.scalatest.funsuite.AnyFunSuite

class Day11Test extends AnyFunSuite {

  val puzzleInput = "5483143223\n2745854711\n5264556173\n6141336146\n6357385478\n4167524645\n2176841721\n6882881134\n4846848554\n5283751526"

  test("Day11.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day11.solve1(input) == 1656)
  }

  test("Day11.solve1_1step") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day11.solve1(input, steps=1) == 0)
  }

  test("Day11.solve1_2step") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day11.solve1(input, steps=2) == 35)
  }

  test("Day11.solve1_10step") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day11.solve1(input, steps=10) == 204)
  }

  test("Day11.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day11.solve2(input) == 195)
  }

}
