package com.raymond.day12

import org.scalatest.funsuite.AnyFunSuite

class Day12Test extends AnyFunSuite {

  val puzzleInput1 = "start-A\nstart-b\nA-c\nA-b\nb-d\nA-end\nb-end"
  val puzzleInput2 = "dc-end\nHN-start\nstart-kj\ndc-start\ndc-HN\nLN-dc\nHN-end\nkj-sa\nkj-HN\nkj-dc"
  val puzzleInput3 = "fs-end\nhe-DX\nfs-he\nstart-DX\npj-DX\nend-zg\nzg-sl\nzg-pj\npj-he\nRW-he\nfs-DX\npj-RW\nzg-RW\nstart-pj\nhe-WI\nzg-he\npj-fs\nstart-RW"

  test("Day12.solve1_1") {
    val input = puzzleInput1.split(raw"\n").iterator

    assert(Day12.solve1(input) == 10)
  }

  test("Day12.solve1_2") {
    val input = puzzleInput2.split(raw"\n").iterator

    assert(Day12.solve1(input) == 19)
  }

  test("Day12.solve1_3") {
    val input = puzzleInput3.split(raw"\n").iterator

    assert(Day12.solve1(input) == 226)
  }

  test("Day12.solve2_1") {
    val input = puzzleInput1.split(raw"\n").iterator

    assert(Day12.solve2(input) == 36)
  }

  test("Day12.solve2_2") {
    val input = puzzleInput2.split(raw"\n").iterator

    assert(Day12.solve2(input) == 103)
  }

  test("Day12.solve2_3") {
    val input = puzzleInput3.split(raw"\n").iterator

    assert(Day12.solve2(input) == 3509)
  }

}
