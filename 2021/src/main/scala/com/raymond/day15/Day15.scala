package com.raymond.day15

import com.raymond.helpers.Input

import scala.collection.mutable.Map
import scala.collection.mutable.PriorityQueue
import scala.Double.PositiveInfinity

object Day15 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day15/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day15/input.txt")
    println(solve2(input2))
  }

  /**
   * Traverse the graph and return the path of least cost (risk in the case of the puzzle).
   *
   * @param nodes mapping of node locations -> cost/risk
   * @param start start location
   * @param end end location (goal)
   * @return iterator of the lowest risk path
   */
  def aStar(nodes: Map[Tuple2[Int, Int], Int], start: Tuple2[Int, Int], end: Tuple2[Int, Int]): Iterator[Tuple2[Int, Int]] = {
    def h(t: Tuple2[Int, Int]) = math.sqrt(math.pow(end(0) - t(0), 2) + math.pow((end(1) - t(1)), 2))

    val cameFrom = Map[Tuple2[Int, Int], Tuple2[Int, Int]]() // for backtracing

    val gScore = Map[Tuple2[Int, Int], Double]()

    val fScore = Map[Tuple2[Int, Int], Double]()
    for node <- nodes do {
      gScore(node(0)) = PositiveInfinity
      fScore(node(0)) = PositiveInfinity
    }

    gScore(start) = 0
    fScore(start) = h(start)
    val openSet = PriorityQueue(start)(Ordering.by((t: Tuple2[Int, Int]) => fScore(t))).reverse // for ascending order

    while !openSet.isEmpty do {
      val curr = openSet.dequeue()
      if curr == end then return getPath(cameFrom, curr)

      val (x,y) = curr
      for
        loc <- Vector((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)) if nodes.contains(loc)
      do
        val tempGScore = gScore(curr) + nodes(loc)
        if tempGScore < gScore(loc) then
          cameFrom(loc) = curr
          gScore(loc) = tempGScore
          fScore(loc) = tempGScore + h(loc)
          if !openSet.exists(_ == loc) then
            openSet.enqueue(loc)
    }

    return Iterator[Tuple2[Int, Int]]()
  }

  /**
   * Reconstruct the path taken.
   *
   * @param cameFrom mapping of a node to its previous node in the path
   * @param end the end node
   * @return the path taken
   */
  def getPath(cameFrom: Map[Tuple2[Int, Int], Tuple2[Int, Int]], end: Tuple2[Int, Int]): Iterator[Tuple2[Int, Int]] = {
    var path = List[Tuple2[Int, Int]]()
    path = end +: path

    var curr = end
    while cameFrom.contains(curr) do {
      curr = cameFrom(curr)
      path = curr +: path
    }
    return path.iterator
  }

  def solve1(input: Iterator[String]): Int = {
    val nodes = Map[Tuple2[Int, Int], Int]()
    var maxI = 0
    var maxJ = 0
    for
      (row, j) <- input.zipWithIndex
    do
      for
        (c, i) <- row.split(raw"").zipWithIndex
      do
        nodes((i, j)) = Integer.parseInt(c)
        maxI = i
        maxJ = j

    aStar(nodes, (0,0), (maxI, maxJ)).map(nodes(_)).sum - nodes((0, 0))
  }

  def solve2(input: Iterator[String]): Int = {
    val (input1, input2) = input.duplicate
    val numCols = input2.next().length

    val nodes = Map[Tuple2[Int, Int], Int]()
    var maxI = 0
    var maxJ = 0
    for
      (row, j) <- input1.zipWithIndex
    do
      for
        (c, i) <- row.split(raw"").zipWithIndex
      do
        for
          r1 <- 0 until 5
        do
          for
            r2 <- 0 until 5
          do
            val (x,y) = (numCols * r1 + i, numCols * r2 + j)
            nodes((x, y)) = (Integer.parseInt(c) + r1 + r2 - 1) % 9 + 1
            maxI = x
            maxJ = y

    aStar(nodes, (0,0), (maxI, maxJ)).map(nodes(_)).sum - nodes((0, 0))
  }

}
