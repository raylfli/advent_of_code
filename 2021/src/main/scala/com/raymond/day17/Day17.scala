package com.raymond.day17

import com.raymond.helpers.Input

object Day17 {

  val targetPattern = raw"target area: x=(-?\d+?)\.\.(-?\d+?), y=(-?\d+?)\.\.(-?\d+?)".r

  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day17/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day17/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    val targetStr = input.next()
    val (x1, x2, y1, y2) = targetStr match {
      case targetPattern(x1, x2, y1, y2) => (
        Integer.parseInt(x1),
        Integer.parseInt(x2),
        Integer.parseInt(y1),
        Integer.parseInt(y2))
      case _ => return -1
    }

    val vy = math.abs(y1) - 1
    vy * (vy + 1) / 2
  }

  def solve2(input: Iterator[String]): Int = {
    val targetStr = input.next()
    val (x1, x2, y1, y2) = targetStr match {
      case targetPattern(x1, x2, y1, y2) => (
        Integer.parseInt(x1),
        Integer.parseInt(x2),
        Integer.parseInt(y1),
        Integer.parseInt(y2))
      case _ => return -1
    }

    var count = 0
    for
      vx <- 0 to math.max(x1, x2)
      vy <- math.min(y1, y2) to (math.abs(y1) - 1)
    do
      val p = new Projectile(vx, vy)
      val goal1 = (x1, y2)
      val goal2 = (x2, y1)
      var points = Vector[Tuple2[Int, Int]]()
      var finished = false
      while (p.x < goal2(0) && p.y > goal2(1)) && !finished do {
        val endPoint = p.next()
        if x1 <= endPoint(0) && endPoint(0) <= x2 && y1 <= endPoint(1) && endPoint(1) <= y2 then
          count += 1
          finished = true
      }

    count
  }

}
