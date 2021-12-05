package com.raymond.day5

import com.raymond.helpers.Input

import scala.collection.mutable.Map
import scala.collection.mutable.Set

object Day5 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day5/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day5/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    val vents = Map[Tuple2[Int, Int], Int]()

    val overlap2 = Set[Tuple2[Int, Int]]()
    for
      line <- input
    do
      for
        vent <- processVentLine(line)
      do
        val prevValue = vents.getOrElseUpdate(vent, 0)
        vents(vent) = prevValue + 1

        if vents(vent) >= 2 then
          overlap2 += vent

    overlap2.size
  }

  def processVentLine(s: String): Iterator[Tuple2[Int, Int]] = {
    val endPoints = s.split(raw"->").map(_.strip())

    val start = endPoints(0).split(raw",").map(Integer.parseInt(_))
    val end = endPoints(1).split(raw",").map(Integer.parseInt(_))

    val xDir = Integer.signum(end(0) - start(0))
    val yDir = Integer.signum(end(1) - start(1))

    if xDir != 0 && yDir != 0 then
      return Iterator[Tuple2[Int, Int]]()

    (
      for (
        x <- start(0) to end(0) by (if xDir == 0 then 1 else xDir);
        y <- start(1) to end(1) by (if yDir == 0 then 1 else yDir)
      ) yield (x, y)
      ).iterator
  }

  def solve2(input: Iterator[String]): Int = {
    val vents = Map[Tuple2[Int, Int], Int]()

    val overlap2 = Set[Tuple2[Int, Int]]()
    for
      line <- input
    do
      for
        vent <- processVentLineDiag(line)
      do
        val prevValue = vents.getOrElseUpdate(vent, 0)
        vents(vent) = prevValue + 1

        if vents(vent) >= 2 then
          overlap2 += vent

    overlap2.size
  }

  def processVentLineDiag(s: String): Iterator[Tuple2[Int, Int]] = {
    val endPoints = s.split(raw"->").map(_.strip())

    val start = endPoints(0).split(raw",").map(Integer.parseInt(_))
    val end = endPoints(1).split(raw",").map(Integer.parseInt(_))

    val xDir = Integer.signum(end(0) - start(0))
    val yDir = Integer.signum(end(1) - start(1))

    if xDir != 0 && yDir != 0 then
      var points = Vector[Tuple2[Int, Int]]()
      var point: Tuple2[Int, Int] = (start(0), start(1))
      while point != (end(0), end(1)) do {
        points = points :+ point
        point = (point(0) + xDir, point(1) + yDir)
      }
      points = points :+ point
      return points.iterator

    (
      for (
        x <- start(0) to end(0) by (if xDir == 0 then 1 else xDir);
        y <- start(1) to end(1) by (if yDir == 0 then 1 else yDir)
      ) yield (x, y)
      ).iterator
  }

}
