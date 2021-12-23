package com.raymond.day22

import com.raymond.helpers.Input

import scala.collection.mutable.ListBuffer

object Day22 {

  val STEP_PATTERN = raw"(on|off) x=(-?\d+?)\.\.(-?\d+?),y=(-?\d+?)\.\.(-?\d+?),z=(-?\d+?)\.\.(-?\d+)$$".r

  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day22/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day22/input.txt")
    println(solve2(input2))
  }

  def parseCubes(input: Iterator[String], boundFilter: Boolean = true): Vector[Cube] = {
    var cubes = Vector.empty[Cube]

    for
      cube <- input
    do
      cube match {
        case STEP_PATTERN(action, x1, x2, y1, y2, z1, z2) => {
          val c = (
            action == "on",
            Integer.parseInt(x1),
            Integer.parseInt(x2),
            Integer.parseInt(y1),
            Integer.parseInt(y2),
            Integer.parseInt(z1),
            Integer.parseInt(z2),
          )
          if !boundFilter || (boundFilter && (c(1) >= -50 && c(2) <= 50
            && c(3) >= -50 && c(4) <= 50
            && c(5) >= -50 && c(6) <= 50)) then
            cubes = cubes :+ new Cube(c(1), c(2), c(3), c(4), c(5), c(6), c(0))
        }
      }

    cubes
  }

  def getFinalVolume(cubes: Vector[Cube]): Long = {
    val totalCubes = new ListBuffer[Cube].empty
    for
      c1 <- cubes
    do
      val newCubes = new ListBuffer[Cube].empty
      for
        c2 <- totalCubes
      do
        val inter = c2.intersect(c1)
        inter match {
          case Some(c) => newCubes.addOne(c)
          case _ =>
        }
      if c1.status then totalCubes.addOne(c1)
      totalCubes.addAll(newCubes)

    totalCubes.map(_.volume).sum
  }

  def solve1(input: Iterator[String]): Long = {
    val cubes = parseCubes(input, boundFilter = true)
    getFinalVolume(cubes)
  }

  def solve2(input: Iterator[String]): Long = {
    val cubes = parseCubes(input, boundFilter = false)
    getFinalVolume(cubes)
  }

}
