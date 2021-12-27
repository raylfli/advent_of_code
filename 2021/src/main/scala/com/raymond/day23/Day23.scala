package com.raymond.day23

import com.raymond.helpers.Input

import scala.Double.PositiveInfinity
import scala.collection.mutable.{PriorityQueue}

object Day23 {

  val charToIndex = Map('A' -> 2, 'B' -> 4, 'C' -> 6, 'D' -> 8)
  val charToEnergy = Map('A' -> 1, 'B' -> 10, 'C' -> 100, 'D' -> 1000)

  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day23/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day23/input.txt")
    println(solve2(input2))
  }

  /**
   * Traverse the graph and return the lowest cost burrow rearrangement.
   *
   * @param start the starting burrow arrangement
   * @return the lowest cost
   */
  def aStar(start: Burrow): Option[Int] = {
    val nodes = scala.collection.mutable.Map[String, Burrow](start.toString -> start)

    val gScore = scala.collection.mutable.Map[String, Double]()

    val fScore = scala.collection.mutable.Map[String, Double]()
    for node <- nodes do {
      gScore(node(0)) = PositiveInfinity
      fScore(node(0)) = 0
    }

    gScore(start.toString) = 0
    fScore(start.toString) = h(start)
    val openSet = PriorityQueue[Burrow](start)(Ordering.by((b: Burrow) => fScore(b.toString))).reverse // for ascending order

    while !openSet.isEmpty do {
      val curr = openSet.dequeue()
      if curr.finished then {
        return Some(curr.cost)
      }

      for
        loc <- getOtherMoves(curr)
      do
        nodes(loc.toString) = loc
        val tempGScore = loc.cost
        if tempGScore < gScore.getOrElseUpdate(loc.toString, PositiveInfinity) then
          gScore(loc.toString) = tempGScore
          fScore(loc.toString) = tempGScore + h(loc)
          if !openSet.exists(_ == loc) then
            openSet.enqueue(loc)
    }

    return None
  }

  /**
   * Retrieves all possible moves from this Burrow.
   *
   * @param b the Burrow to find moves for
   * @return Burrows representing all possible moves
   */
  def getOtherMoves(b: Burrow): Vector[Burrow] = {
    var possibleMoves = Vector[Burrow]()
    // check hallway to room moves (always best)
    for
      (c,i) <- b.hallway.zipWithIndex
    do
      c match {
        case 'A' | 'B' | 'C' | 'D' => if b.rooms(c).forall((a: Char) => a == c) then
          if (i < charToIndex(c) && b.hallway.slice(i + 1, charToIndex(c)).forall((a: Char) => a == '.')) || (i > charToIndex(c) && b.hallway.slice(charToIndex(c), i).forall((a: Char) => a == '.')) then
            val moves = math.abs(charToIndex(c) - i) + b.maxSize - b.rooms(c).size
            val cost = moves * charToEnergy(c)

            val newHallway = b.hallway.slice(0, i) + '.' + b.hallway.slice(i + 1, b.hallway.length)
            val newRooms = b.rooms.updated(c, b.rooms(c) + c)
            possibleMoves = possibleMoves :+ new Burrow(b.maxSize, newHallway, newRooms, b.cost + cost)
        case _ =>
      }

    // next best is room to room
    for
      (room, fill) <- b.rooms
    do
      if fill.length > 0 && fill(0) != room && b.rooms(fill(0)).forall(_ == fill(0)) then
        val c = fill(0)
        if (charToIndex(room) < charToIndex(c) && b.hallway.slice(charToIndex(room), charToIndex(c) + 1).forall(_ == '.')) || (charToIndex(room) > charToIndex(c) && b.hallway.slice(charToIndex(c), charToIndex(room) + 1).forall(_ == '.')) then
          val leaveRoom = b.maxSize - fill.size + 1
          val moveHallway = math.abs(charToIndex(c) - charToIndex(room))
          val intoRoom = b.maxSize - b.rooms(c).size
          val cost = (leaveRoom + moveHallway + intoRoom) * charToEnergy(c)

          val newRooms = b.rooms.updated(room, fill.slice(1, fill.size)).updated(c, b.rooms(c) + c)
          possibleMoves = possibleMoves :+ new Burrow(b.maxSize, b.hallway, newRooms, b.cost + cost)

    // finally, only other move is from room to some hallway position
    val hallwayPos = Vector(0, 1, 3, 5, 7, 9, 10)
    for
      (room, fill) <- b.rooms
    do
      var thisRoomPossibleMoves = Vector[Burrow]()
      if fill.length > 0 && fill.exists(_ != room) then
        for
          pos <- hallwayPos
        do
          if b.hallway(pos) == '.' then
            if (pos < charToIndex(room) && b.hallway.slice(pos, charToIndex(room) + 1).forall(_ == '.')) || (pos > charToIndex(room) && b.hallway.slice(charToIndex(room), pos).forall(_ == '.') ) then
              val c = fill(0)
              val leaveRoom = b.maxSize - fill.size + 1
              val moveHallway = math.abs(charToIndex(room) - pos)
              val cost = (leaveRoom + moveHallway) * charToEnergy(c)

              val newHallway = b.hallway.slice(0, pos) + c + b.hallway.slice(pos + 1, b.hallway.length)
              val newRooms = b.rooms.updated(room, fill.slice(1, fill.size))
              thisRoomPossibleMoves = thisRoomPossibleMoves :+ new Burrow(b.maxSize, newHallway, newRooms, b.cost + cost)

      possibleMoves = possibleMoves :++ thisRoomPossibleMoves

    possibleMoves
  }

  /**
   * Heuristic cost of organizing this Burrow.
   *
   * @param b the Burrow to estimate remaining cost for
   * @return the estimated cost
   */
  def h(b: Burrow): Double = {
    if b.finished then return 0
    var cost = 0
    for
      (c, i) <- b.hallway.zipWithIndex
    do
      c match {
        case 'A' | 'B' | 'C' | 'D' => cost += (math.abs(charToIndex(c) - i) * charToEnergy(c))
        case _ =>
      }

    for
      (room, fill) <- b.rooms
    do
      if fill.size > 0 then
        val c = fill(0)

        val leaveRoom = b.maxSize - fill.size + 1
        val moveHallway = math.abs(charToIndex(room) - charToIndex(c))
        cost += (leaveRoom + moveHallway) * charToEnergy(c)

    cost
  }


  def solve1(input: Iterator[String]): Int = {
    input.next() // blank line
    val hallwayRaw = input.next()
    val hallway = hallwayRaw.slice(1, hallwayRaw.length - 1)

    var rooms = Map[Char, String]('A' -> "", 'B' -> "", 'C' -> "", 'D' -> "")
    while input.hasNext do {
      val line = input.next()
      if line(3).isLetter then
        rooms = rooms.updated('A', rooms('A') + line(3)).updated('B', rooms('B') + line(5)).updated('C', rooms('C') + line(7)).updated('D', rooms('D') + line(9))
    }

    val b = new Burrow(rooms('A').length, hallway, rooms)

    aStar(b) match {
      case Some(i) => i
      case _ => -1
    }
  }

  def solve2(input: Iterator[String]): Int = {
    val input2 = input.toVector
    val newLines = "  #D#C#B#A#\n  #D#B#A#C#".split(raw"\n").toVector
    val input3 = (input2.slice(0, 3) :++ newLines :++ input2.slice(3, input2.size)).iterator

    solve1(input3)
  }

}
