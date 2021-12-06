package com.raymond.day6

import com.raymond.helpers.Input

import scala.collection.mutable
import scala.collection.mutable.Map

object Day6 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day6/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day6/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Long = {
    simulateLanternFish(getStartStateMap(input), 80)
  }

  private def getStartStateMap(input: Iterator[String]) = {
    val initialState = input.next().split(raw",").iterator.map(Integer.parseInt(_))
    val fishCounts: mutable.Map[Int, Long] = Map[Int, Long]()

    for
      fish <- initialState
    do
      val state = fishCounts.getOrElseUpdate(fish, 0)
      fishCounts(fish) = state + 1

    fishCounts
  }

  private def simulateLanternFish(fishCounts: mutable.Map[Int, Long], numDays: Int) = {
    for
      day <- 1 to numDays
    do
      for
        state <- 0 to 9
      do
        if state == 0 then
          val numFish = fishCounts.getOrElseUpdate(state, 0)
          fishCounts(7) = fishCounts.getOrElseUpdate(7, 0) + numFish
          fishCounts(9) = numFish
        else // state > 0
          fishCounts(state - 1) = fishCounts.getOrElseUpdate(state, 0)

      fishCounts(9) = 0

    fishCounts.values.map(_.toLong).sum
  }

  def solve2(input: Iterator[String]): Long = {
    simulateLanternFish(getStartStateMap(input), 256)
  }

}
