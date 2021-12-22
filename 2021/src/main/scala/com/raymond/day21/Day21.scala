package com.raymond.day21

import com.raymond.helpers.Input

import scala.annotation.tailrec

object Day21 {

  val PLAYER_START_PATTERN = raw"Player (\d) starting position: (\d)".r

  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day21/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day21/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    var scores = Map[Int, Int]()
    var positions = Map[Int, Int]()

    while input.hasNext do {
      input.next() match {
        case PLAYER_START_PATTERN(num, pos) => {
          val (player, position) = (Integer.parseInt(num), Integer.parseInt(pos))
          positions = positions + (player -> position)
          scores = scores + (player -> 0)
        }
      }
    }

    val d = new DeterministicDie()

    var p = 1 // assuming only 2 players
    val pMax = 2
    while true do {
      val rollTotal = (for n <- 1 to 3 yield d.next()).sum
      val newPos = (positions(p) - 1 + rollTotal) % 10 + 1
      positions = positions.updated(p, newPos)
      scores = scores.updated(p, scores(p) + newPos)

      if scores(p) >= 1000 then
        return scores(p % pMax + 1) * d.totalNumRolls

      p = p % pMax + 1 // get next player
    }
    -1
  }

  def solve2(input: Iterator[String]): Long = {
    var positions = Map[Int, Int]()

    while input.hasNext do {
      input.next() match {
        case PLAYER_START_PATTERN(num, pos) => {
          val (player, position) = (Integer.parseInt(num), Integer.parseInt(pos))
          positions = positions + (player -> position)
        }
      }
    }

    val (wins1, wins2) = playGame(positions(1), positions(2))
    math.max(wins1, wins2)
  }

  val sums = (
    for
      a <- 1 to 3
      b <- 1 to 3
      c <- 1 to 3
    yield
      a + b + c
    ).toVector.groupBy((s: Int) => s).map((n: Int, v: Vector[Int]) => (n, v.length))

  val cache = scala.collection.mutable.Map.empty[(Int, Int, Int, Int), (Long, Long)]

  def playGame(pos1: Int, pos2: Int, score1: Int = 0, score2: Int = 0): (Long, Long) = cache.getOrElseUpdate(
    (pos1, pos2, score1, score2),
    if score2 >= 21 then
      (0L, 1L)
    else
      sums.foldLeft((0L, 0L)) {
        case ((wins1, wins2), (move, n)) => {
          val newPos = (pos1 - 1 + move) % 10 + 1
          val (w2, w1) = playGame(pos2, newPos, score2, score1 + newPos)
          (wins1 + n * w1, wins2 + n * w2)
        }
      }
  )

}
