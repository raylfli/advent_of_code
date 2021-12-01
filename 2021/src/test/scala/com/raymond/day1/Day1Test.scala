package com.raymond.day1

import org.scalatest.funsuite.AnyFunSuite

class Day1Test extends AnyFunSuite {

  test("Day1.solve1") {
    val input = "199\n200\n208\n210\n200\n207\n240\n269\n260\n263".split(raw"\n").iterator

    assert(7 == Day1.solve1(input))
  }

  test("Day1.solve2") {
    val input = "199\n200\n208\n210\n200\n207\n240\n269\n260\n263".split(raw"\n").iterator

    assert(5 == Day1.solve2(input))
  }

}
