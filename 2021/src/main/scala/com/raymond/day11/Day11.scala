package com.raymond.day11

import com.raymond.helpers.Input

import scala.collection.mutable.Map
import scala.collection.mutable.Set

object Day11 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day11/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day11/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String], steps: Int = 100): Int = {
    var octopuses = Map[Tuple2[Int, Int], Int]()

    for
      (row, i) <- input.zipWithIndex
    do
      for
        (energy, j) <- row.split(raw"").zipWithIndex
      do
        octopuses(Tuple2(i, j)) = Integer.parseInt(energy)

    (for stepNum <- 1 to steps yield step(octopuses)).sum
  }

  /**
   * Complete one step.
   *
   * @param octopuses mapping of octopus location to energy level
   * @return the number of flashes in this step
   */
  def step(octopuses: Map[Tuple2[Int, Int], Int]): Int = {
    for
      (loc, energy) <- octopuses
    do
      octopuses(loc) += 1

    var flashed = Set[Tuple2[Int, Int]]()
    var stepFlashes = 0

    for
      (loc, energy) <- octopuses
    do
      stepFlashes += checkFlashes(octopuses, loc, flashed)

    for
      loc <- flashed
    do
      octopuses(loc) = 0

//    printOctopuses(octopuses)
    stepFlashes
  }

  /**
   * Check if this octopus should flash and recursively compute the total number of flashes.
   *
   * @param octopuses mapping of octopus location to their energy level (gets mutated)
   * @param octopus octopus to check and propagate from
   * @param flashed octopuses that have already flashed this step (gets mutated)
   * @return the number of flashes this step
   */
  def checkFlashes(octopuses: Map[Tuple2[Int, Int], Int], octopus: Tuple2[Int, Int], flashed: Set[Tuple2[Int, Int]]): Int = {
    if octopuses(octopus) <= 9 || flashed.contains(octopus) then
      return 0

    flashed.add(octopus)

    val x = octopus(0)
    val y = octopus(1)

    var toCheck = Vector[Tuple2[Int, Int]]()
    for
      i <- x - 1 to x + 1
    do
      for
        j <- y - 1 to y + 1
      do
        val loc = Tuple2(i, j)
        if loc != octopus && octopuses.contains(loc) && !flashed.contains(loc) then
          toCheck = toCheck :+ loc

    var flashes = 1  // current octopus has flashed
    for
      check <- toCheck
    do
      octopuses(check) += 1
      flashes += checkFlashes(octopuses, check, flashed)

    flashes
  }

  /**
   * Pretty print this mapping of octopuses.
   *
   * @param octopuses
   */
  def printOctopuses(octopuses: Map[Tuple2[Int, Int], Int]): Unit = {
    var i = 0
    var j = 0
    while octopuses.contains(Tuple2(i, 0)) do {
      while octopuses.contains(Tuple2(i, j)) do {
        print(octopuses(Tuple2(i, j)))
        j += 1
      }
      j = 0
      i += 1
      println("")
    }
    println("")
  }

  def solve2(input: Iterator[String]): Int = {
    var octopuses = Map[Tuple2[Int, Int], Int]()

    for
      (row, i) <- input.zipWithIndex
    do
      for
      (energy, j) <- row.split(raw"").zipWithIndex
    do
      octopuses(Tuple2(i, j)) = Integer.parseInt(energy)

    var steps = 1
    while step(octopuses) != 100 do {
      steps += 1
    }

    steps
  }

}
