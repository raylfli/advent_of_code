package com.raymond.day24

import com.raymond.helpers.Input

object Day24 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day24/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day24/input.txt")
    println(solve2(input2))
  }

  def parseVariables(input: Iterator[String]): Tuple3[Vector[Int], Vector[Int], Vector[Int]] = {
    val inputStr = input.toVector

    var modes = Vector[Int]()
    var checks = Vector[Int]()
    var offsets = Vector[Int]()

    val instructionOffset = 18
    for i <- 0 until 14 do {
      modes = modes :+ inputStr(instructionOffset * i + 4).split(raw" ")(2).toInt
      checks = checks :+ inputStr(instructionOffset * i + 5).split(raw" ")(2).toInt
      offsets = offsets :+ inputStr(instructionOffset * i + 15).split(raw" ")(2).toInt
    }

    (modes, checks, offsets)
  }

  def getOptimalNumber(modes: Vector[Int], checks: Vector[Int], offsets: Vector[Int], getMax: Boolean = true): Long = {
    var num = Vector(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    var stack = List.empty[Tuple2[Int, Int]]
    for
      i <- 0 until 14
    do
      val (mode, check, offset) = (modes(i), checks(i), offsets(i))
      mode match {
        case 1 => {
          stack = stack :+ (i, offset)
        }

        case 26 =>
          val (popI, offsetI) = stack.last
          stack = stack.dropRight(1)

          if getMax then
            val diff = offsetI + check
            num = num.updated(popI, 9 - math.max(0, diff))
            num = num.updated(i, 9 + math.min(0, diff))
          else
            val diff = offsetI + check
            num = num.updated(popI, 1 - math.min(0, diff))
            num = num.updated(i, 1 + math.max(0, diff))
      }

    num.foldLeft(0L)((prev: Long, next: Int) => prev * 10 + next)
  }

  def solve1(input: Iterator[String]): Long = {
    val (modes, checks, offsets) = parseVariables(input)
    getOptimalNumber(modes, checks, offsets)
  }

  def solve2(input: Iterator[String]): Long = {
    val (modes, checks, offsets) = parseVariables(input)
    getOptimalNumber(modes, checks, offsets, getMax = false)
  }

}
