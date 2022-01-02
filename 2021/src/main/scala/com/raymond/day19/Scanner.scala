package com.raymond.day19

import scala.collection.mutable.Map

class Scanner(initBeacons: Vector[Tuple3[Int, Int, Int]]) {

  var beacons = initBeacons

  var connections: Map[Tuple2[Tuple3[Int, Int, Int], Tuple3[Int, Int, Int]], Tuple3[Int, Int, Int]] = {
    val m = Map.empty[Tuple2[Tuple3[Int, Int, Int], Tuple3[Int, Int, Int]], Tuple3[Int, Int, Int]]
    for
      ((x1, y1, z1), i) <- beacons.zipWithIndex
      ((x2, y2, z2), j) <- beacons.zipWithIndex
      if i != j
    do
      m.addOne(((x1, y1, z1), (x2, y2, z2)) -> (x1 - x2, y1 - y2, z1 - z2))

    m
  }

  def addBeacons(newBeacons: Vector[Tuple3[Int, Int, Int]]): Unit = {
    for
      (x1, y1, z1) <- newBeacons
      (x2, y2, z2) <- beacons
    do
      connections.addOne(((x1, y1, z1), (x2, y2, z2)) -> (x1 - x2, y1 - y2, z1 - z2))

    for
      ((x1, y1, z1), i) <- newBeacons.zipWithIndex
      ((x2, y2, z2), j) <- newBeacons.zipWithIndex
      if i != j
    do
      connections.addOne(((x1, y1, z1), (x2, y2, z2)) -> (x1 - x2, y1 - y2, z1 - z2))

    beacons = beacons :++ newBeacons
  }

  override def toString: String = s"Scanner: ${beacons.toString()}"

}
