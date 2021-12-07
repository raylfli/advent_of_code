package com.raymond.day7

import com.raymond.helpers.Input

import scala.math.{abs, min, signum}

object Day7 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day7/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day7/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    val inputList = input.next().split(raw",").toList.map(Integer.parseInt(_))
    val sortedInput = inputList.sorted

    // median will minimize absolute distance
    if sortedInput.size % 2 == 1 then
      val median = sortedInput(sortedInput.size / 2)
      sortedInput
        .map(_ - median)
        .map(abs)
        .sum
    else
      val median1 = sortedInput(sortedInput.size / 2)
      val median2 = sortedInput(sortedInput.size / 2 + 1)

      min(sortedInput
        .map(_ - median1)
        .map(abs)
        .sum,
        sortedInput
          .map(_ - median2)
          .map(abs)
          .sum)
  }

  def solve2(input: Iterator[String]): Int = {
    val inputList = input.next().split(raw",").toList.map(Integer.parseInt(_))
    val sortedInput = inputList.sorted

    // increasing fuel costs should place the optimal position away from the median and towards the mean
    // since the mean is more sensitive to outliers (farther positions should be "weighted" higher)
    // still looking for a global minimum
    val mean = inputList.sum / inputList.size
    val median = sortedInput(sortedInput.size / 2)

    val direction = signum(mean - median)

    var previous = sortedInput
      .map((x: Int) => abs(x - median) + 1)
      .map((x: Int) => x * (x - 1) / 2)  // sum of nums from 0 to (x + 1)
      .sum

    var check = median + direction
    var next = sortedInput
      .map((x: Int) => abs(x - check) + 1)
      .map((x: Int) => x * (x - 1) / 2)  // sum of nums from 0 to (x + 1)
      .sum

    while previous >= next do {
      previous = next
      check = check + direction
      next = sortedInput
        .map((x: Int) => abs(x - check) + 1)
        .map((x: Int) => x * (x - 1) / 2)  // sum of nums from 0 to (x + 1)
        .sum
    }

    previous
  }

}
