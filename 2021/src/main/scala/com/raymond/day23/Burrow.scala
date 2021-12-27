package com.raymond.day23

case class Burrow(maxSize: Int, hallway: String, rooms: Map[Char, String], cost: Int = 0) {

  val finished = rooms.forall((t: Char, spots: String) => spots.size == maxSize && spots.forall(_ == t))

  override def toString: String = hallway.toString() + ' ' + rooms('A').toString() + ' ' + rooms('B').toString() + ' ' + rooms('C').toString() + ' ' + rooms('D').toString()

}
