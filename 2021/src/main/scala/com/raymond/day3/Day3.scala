package com.raymond.day3

import com.raymond.helpers.Input

import scala.collection.mutable.ArrayBuffer
import scala.collection.mutable.Map

object Day3 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day3/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day3/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    val inputList = input.toList
    var counts = ArrayBuffer.fill(inputList(0).length)(0)

    for
      c <- 0 until inputList(0).length
    do
      for
        s <- inputList
      do
        if s(c) == '1' then
          counts(c) += 1
        else
          counts(c) -= 1

    counts = counts.map((c: Int) => if c > 0 then 1 else 0)

    val gammaBinary = counts.mkString
    val gammaInt = Integer.parseInt(gammaBinary, 2)

    val epsilonBinary = gammaBinary.map((c: Char) => if c == '0' then '1' else '0')
    val epsilonInt = Integer.parseInt(epsilonBinary, 2)

    gammaInt * epsilonInt
  }

  def solve2(input: Iterator[String]): Int = {
    var inputList = input.toVector


    rating(inputList, "oxy") * rating(inputList, "co2")
  }

  /**
   * Returns rating of the specified system and input data.
   * @param input input data
   * @param system system to get the rating for (one of "oxy" or "co2")
   * @return the rating of the specified system
   */
  def rating(input: Vector[String], system: String, i: Int = 0): Int = {
    if input.size == 1 then
      return Integer.parseInt(input(0), 2)

    val filtered = Map('0' -> Vector[String](), '1' -> Vector[String]())
    for
      s <- input
    do
      filtered(s(i)) = filtered(s(i)) :+ s

    val larger = if filtered('1').size >= filtered('0').size then '1' else '0'
    val smaller = if larger == '0' then '1' else '0'
    if system == "oxy" then
      return rating(filtered(larger), system, i=i + 1)
    else
      return rating(filtered(smaller), system, i=i + 1)
  }

}
