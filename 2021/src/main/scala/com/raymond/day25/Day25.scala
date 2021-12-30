package com.raymond.day25

import com.raymond.helpers.Input

import scala.collection.mutable.Map

object Day25 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day25/input.txt")
    println(solve1(input1))

    // NO PART 2 PUZZLE
//    val input2 = Input.getInput("src/main/scala/com/raymond/day25/input.txt")
//    println(solve2(input2))
  }

  def step(cucumbers: Map[Tuple2[Int, Int], Byte], maxX: Int, maxY: Int): Tuple2[Map[Tuple2[Int, Int], Byte], Boolean]= {
    // east = 1
    // south = -1

    val eastMoves = Map[Tuple2[Int, Int], Byte]()
    var moved = false
    for
      ((x, y), b) <- cucumbers
    do
      val loc = ((x + 1) % maxX, y)
      if b == 1 && !cucumbers.contains(loc) then
        moved = true
        eastMoves(loc) = b
      else if !eastMoves.contains((x, y)) then
        eastMoves((x, y)) = b

    val southMoves = Map[Tuple2[Int, Int], Byte]()
    for
      ((x, y), b) <- eastMoves
    do
      val loc = (x, (y + 1) % maxY)
      if b == -1 && !eastMoves.contains(loc) then
        moved = true
        southMoves(loc) = b
      else if !southMoves.contains((x, y)) then
        southMoves((x, y)) = b

    (southMoves, moved)
  }

  def stringToCucumbers(input: Iterator[String]): Tuple3[Map[Tuple2[Int, Int], Byte], Int, Int] = {
    var j = 0
    var maxX = 0
    var maxY = 0

    var cucumbers = Map[Tuple2[Int, Int], Byte]()

    while input.hasNext do {
      for
        (c, i) <- input.next().zipWithIndex
      do
        if c == '>' then cucumbers((i, j)) = 1
        if c == 'v' then cucumbers((i, j)) = -1
        maxX = math.max(maxX, i)

      j += 1
    }
    maxY = j

    (cucumbers, maxX + 1, maxY)
  }

  def solve1(input: Iterator[String]): Int = {
    var (cucumbers, maxX, maxY) = stringToCucumbers(input)

    var count = 0
    var moved = true
    while moved do {
      val stepResult = step(cucumbers, maxX, maxY)
      cucumbers = stepResult(0)
      moved = stepResult(1)
      count += 1
    }

    count
  }

// NO PART 2 PUZZLE
//  def solve2(input: Iterator[String]): Int = {
//    -1
//  }

}
