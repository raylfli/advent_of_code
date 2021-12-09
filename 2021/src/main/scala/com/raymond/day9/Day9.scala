
package com.raymond.day9

import com.raymond.helpers.Input

import scala.collection.mutable.Set

object Day9 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day9/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day9/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    var prevRow: Option[Vector[Int]] = None
    var currRow: Option[Vector[Int]] = Option(input.next().split(raw"").map(Integer.parseInt(_)).toVector)
    var nextRow: Option[Vector[Int]] = Option(input.next().split(raw"").map(Integer.parseInt(_)).toVector)

    var risk = 0
    while currRow match {case Some(r) => true case _ => false} do {
      for
        t <- currRow.getOrElse(Vector[Int]()).zipWithIndex
      do
        if t(0) == 0 then
          risk += 1
        else if currRow match {case Some(r) => isLow(prevRow, r, nextRow, t(1)) case _ => false} then
          risk += t(0) + 1

      prevRow = currRow
      currRow = nextRow
      try {
        nextRow = Option(input.next().split(raw"").map(Integer.parseInt(_)).toVector)
      } catch {
        case e: NoSuchElementException => nextRow = None
      }
    }

    risk
  }

  private def isLow(prevRow: Option[Vector[Int]], currRow: Vector[Int], nextRow: Option[Vector[Int]], i: Int): Boolean = {
    if (prevRow match {
      case Some(r) => currRow(i) > r(i)
      case _ => false
    }) then
      return false

    if (nextRow match {
      case Some(r) => currRow(i) > r(i)
      case _ => false
    }) then
      return false

    (i == 0 || currRow(i) < currRow(i - 1)) && (i == currRow.length - 1 || currRow(i) < currRow(i + 1))
  }

  def solve2(input: Iterator[String]): Int = {
    val locations = Set[Tuple2[Int, Int]]()

    for
      (row, i) <- input.zipWithIndex
    do
      for
        (num, j) <- row.split(raw"").map(Integer.parseInt(_)).zipWithIndex
      do
        if num != 9 then
          locations += Tuple2(i, j)

    var basinSizes = Vector[Int]()

    while locations.size != 0 do {
      val root = locations.iterator.next()
      val size = findBasinSize(root, locations)
      basinSizes = basinSizes :+ size

    }

    basinSizes.sortWith((a: Int, b: Int) => a > b).slice(0, 3).product
  }

  private def findBasinSize(root: Tuple2[Int, Int], locations: Set[Tuple2[Int, Int]], size: Int = 0): Int = {
    val (x, y) = root
    locations -= root
    var basin = size + 1

    if locations.contains((x - 1, y)) then
      basin += findBasinSize((x - 1, y), locations)

    if locations.contains((x + 1, y)) then
      basin += findBasinSize((x + 1, y), locations)

    if locations.contains((x, y - 1)) then
      basin += findBasinSize((x, y - 1), locations)

    if locations.contains((x, y + 1)) then
      basin += findBasinSize((x, y + 1), locations)

    basin
  }

}
