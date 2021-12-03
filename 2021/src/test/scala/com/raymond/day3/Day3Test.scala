package com.raymond.day3

import org.scalatest.funsuite.AnyFunSuite

class Day3Test extends AnyFunSuite {

  val puzzleInput = "00100\n11110\n10110\n10111\n10101\n01111\n00111\n11100\n10000\n11001\n00010\n01010"

  test("Day3.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day3.solve1(input) == 198)
  }

  test("Day3.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day3.solve2(input) == 230)
  }

}
