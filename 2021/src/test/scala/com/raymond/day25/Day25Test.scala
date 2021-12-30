package com.raymond.day25

import org.scalatest.funsuite.AnyFunSuite

class Day25Test extends AnyFunSuite {

  val puzzleInput = "v...>>.vv>\n.vv>>.vv..\n>>.>v>...v\n>>v>>.>.v.\nv>v.vv.v..\n>.>>..v...\n.vv..>.>v.\nv.v..>>v.v\n....v..v.>"

  test("Day25.step_1") {
    val input = "...>>>>>...".split(raw"\n").iterator
    val (cucumbers, maxX, maxY) = Day25.stringToCucumbers(input)

    val (newCucumbers, moved) = Day25.step(cucumbers, maxX, maxY)

    val input2 = "...>>>>.>..".split(raw"\n").iterator
    val (cucumbers2, maxX2, maxY2) = Day25.stringToCucumbers(input2)
    assert(newCucumbers == cucumbers2)
  }

  test("Day25.step_2") {
    val input = "..........\n.>v....v..\n.......>..\n..........".split(raw"\n").iterator
    val (cucumbers, maxX, maxY) = Day25.stringToCucumbers(input)

    val (newCucumbers, moved) = Day25.step(cucumbers, maxX, maxY)

    val input2 = "..........\n.>........\n..v....v>.\n..........".split(raw"\n").iterator
    val (cucumbers2, maxX2, maxY2) = Day25.stringToCucumbers(input2)
    assert(newCucumbers == cucumbers2)
  }

  test("Day25.step_3") {
    val input = "...>...\n.......\n......>\nv.....>\n......>\n.......\n..vvv..".split(raw"\n").iterator
    val (cucumbers, maxX, maxY) = Day25.stringToCucumbers(input)

    val (newCucumbers, moved) = Day25.step(cucumbers, maxX, maxY)

    val input2 = "..vv>..\n.......\n>......\nv.....>\n>......\n.......\n....v..".split(raw"\n").iterator
    val (cucumbers2, maxX2, maxY2) = Day25.stringToCucumbers(input2)
    assert(newCucumbers == cucumbers2)
  }

  test("Day25.noMovement") {
    val input = "..>>v>vv..\n..v.>>vv..\n..>>v>>vv.\n..>>>>>vv.\nv......>vv\nv>v....>>v\nvvv.....>>\n>vv......>\n.>v.vv.v..".split(raw"\n").iterator
    val (cucumbers, maxX, maxY) = Day25.stringToCucumbers(input)
    val (newCucumbers, moved) = Day25.step(cucumbers, maxX, maxY)

    assert(!moved)
    assert(cucumbers == newCucumbers)
  }

  test("Day25.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day25.solve1(input) == 58)
  }

// NO PART 2 PUZZLE
//  test("Day25.solve2") {
//    val input = puzzleInput.split(raw"\n").iterator
//
//    assert(Day25.solve2(input) == 404)
//  }

}
