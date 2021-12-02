package com.raymond.day2

import com.raymond.helpers.Input

object Day2 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day2/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day2/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    var horizontal = 0
    var depth = 0

    for
      s <- input
    do
      var command = s.split(raw" ")
      var translation = command(1).toInt
      command(0) match {
        case "forward" => horizontal += translation
        case "down" => depth += translation
        case "up" => depth -= translation
      }

    horizontal * depth
  }

  def solve2(input: Iterator[String]): Int = {
    var horizontal = 0
    var depth = 0
    var aim = 0

    for
      s <- input
    do
      var command = s.split(raw" ")
      var translation = command(1).toInt
      command(0) match {
        case "forward" => {
          horizontal += translation
          depth += translation * aim
        }
        case "down" => aim += translation
        case "up" => aim -= translation
      }

    horizontal * depth
  }

}
