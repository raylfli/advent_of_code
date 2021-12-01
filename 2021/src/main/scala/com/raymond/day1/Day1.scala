package com.raymond.day1

import com.raymond.helpers.Input

object Day1 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day1/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day1/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    val inputInts = input.map(_.toInt).toList

    var count = 0
    for i <- 1 until inputInts.length if inputInts(i) > inputInts(i - 1) do count += 1

    count
  }

  def solve2(input: Iterator[String]): Int = {
    val inputInts = input.map(_.toInt).toList

    var count = 0

    var window1 = inputInts(0) + inputInts(1) + inputInts(2)
    var window2 = 0
    for
      i <- 3 until inputInts.length
    do
      window2 = window1 - inputInts(i - 3) + inputInts(i)
      if window2 > window1 then
        count += 1

      window1 = window2

    count
  }

}
