package com.raymond.day13

import com.raymond.helpers.Input

import scala.collection.mutable.Set
import scala.math.Ordering.Implicits.*
import scala.math.abs

object Day13 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day13/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day13/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    var points = Set[Tuple2[Int, Int]]() // set of points (x, y)

    var row = input.next()
    while row != "" do {
      val split = row.split(raw",")
      points.add(Tuple2(Integer.parseInt(split(0)), Integer.parseInt(split(1))))
      row = input.next()
    }

    var folds = Vector[Tuple2[String, Int]]() // fold locations (axis, location)
    while input.hasNext do {
      val split = input.next().split(raw" ")
      val foldLocation = split(2).split(raw"=")
      folds = folds :+ Tuple2(foldLocation(0), Integer.parseInt(foldLocation(1)))
    }

    // just one fold for this problem
    points = fold(points, folds(0))

    points.size
  }

  /**
   * Compute the new points after a fold is executed.
   *
   * @param points Set of points on the paper (x,y)
   * @param line   line to fold over (axis, location)
   */
  def fold(points: Set[Tuple2[Int, Int]], line: Tuple2[String, Int]): Set[Tuple2[Int, Int]] = {
    var pointMap = (l: Int, t: Tuple2[Int, Int]) => Tuple2(t._1, t._2)
    if line(0) == "x" then
      pointMap = (l: Int, t: Tuple2[Int, Int]) => Tuple2(l - abs(l - t._1), t._2)
    else
      pointMap = (l: Int, t: Tuple2[Int, Int]) => Tuple2(t._1, l - abs(l - t._2))

    points.map((t: Tuple2[Int, Int]) => pointMap(line._2, t))
  }

  def solve2(input: Iterator[String]): String = {
    var points: Set[Tuple2[Int, Int]] = Set[Tuple2[Int, Int]]() // set of points (x, y)

    var row = input.next()
    while row != "" do {
      val split = row.split(raw",")
      points.add(Tuple2(Integer.parseInt(split(0)), Integer.parseInt(split(1))))
      row = input.next()
    }

    var folds = Vector[Tuple2[String, Int]]() // fold locations (axis, location)
    while input.hasNext do {
      val split = input.next().split(raw" ")
      val foldLocation = split(2).split(raw"=")
      folds = folds :+ Tuple2(foldLocation(0), Integer.parseInt(foldLocation(1)))
    }

    for
      f <- folds
    do
      points = fold(points, f)

    getCode(points)
  }

  /**
   * Generate a String corresponding to this set of points
   *
   * @param points set of points to plot
   * @return a String representing the given set of points ('#' characters are points, ' ' are blank spaces)
   */
  def getCode(points: Set[Tuple2[Int, Int]]): String = {
    val sortedPoints = points.toVector.sortWith((a: Tuple2[Int, Int], b: Tuple2[Int, Int]) => a < b)
    val maxX = sortedPoints.map((x: Int, y: Int) => x).max
    val maxY = sortedPoints.map((x: Int, y: Int) => y).max

    val builder = new StringBuilder()
    for
      y <- 0 to maxY
    do
      for
        x <- 0 to maxX
      do
        if sortedPoints.contains((x, y)) then
          builder.append('#')
        else
          builder.append(' ')

      builder.append("\n")

    builder.toString
  }

}
