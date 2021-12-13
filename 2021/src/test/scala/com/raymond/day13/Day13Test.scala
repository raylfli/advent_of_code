package com.raymond.day13

import org.scalatest.funsuite.AnyFunSuite

import scala.collection.mutable.Set

class Day13Test extends AnyFunSuite {

  val puzzleInput = "6,10\n0,14\n9,10\n0,3\n10,4\n4,11\n6,0\n6,12\n4,1\n0,13\n10,12\n3,4\n3,0\n8,4\n1,10\n2,14\n8,10\n9,0\n\nfold along y=7\nfold along x=5"

  test("Day13.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day13.solve1(input) == 17)
  }

  test("Day13.fold_y") {
    val points = Set[Tuple2[Int, Int]](Tuple2(0, 14), Tuple2(54, 3))
    val line = Tuple2("y", 7)

    assert(Day13.fold(points, line) == Set(Tuple2(0, 0), Tuple2(54, 3)))
  }

  test("Day13.fold_x") {
    val points = Set[Tuple2[Int, Int]](Tuple2(0, 0), Tuple2(10, 367))
    val line = Tuple2("x", 5)

    assert(Day13.fold(points, line) == Set(Tuple2(0, 0), Tuple2(0, 367)))
  }

  test("Day13.solve2") {
    val input = puzzleInput.split(raw"\n").iterator
    val expected = "#####\n#   #\n#   #\n#   #\n#####\n"

    assert(Day13.solve2(input) == expected)
  }

}
