package com.raymond.day19

import com.raymond.helpers.Input

import scala.collection.mutable.Set
import scala.collection.parallel.CollectionConverters._

import java.util.concurrent.TimeUnit

object Day19 {
  @main def main = {
    val input = Input.getInput("src/main/scala/com/raymond/day19/input.txt")

//    val t1 = System.nanoTime()
    val sol = solve(input)
//    val t2 = System.nanoTime()

//    println(s"Duration (ms): ${TimeUnit.NANOSECONDS.toMillis(t2 - t1)}")
    println(sol(0))
    println(sol(1))
  }

  def matchBeacons(sc1: Scanner, sc2: Scanner): Tuple3[Set[Tuple3[Int, Int, Int]], Tuple3[Int, Int, Int], Tuple3[Int, Int, Int]] = {
    val matching = Set.empty[Tuple3[Int, Int, Int]]
    var displacementV = (0, 0, 0)
    var scannerLoc = (0, 0, 0)

    for
      (points1, v1) <- sc1.connections
      (points2, v2) <- sc2.connections
    do
      if v1 == v2 then
        matching.add(points1(0))
        matching.add(points1(1))
        val (source1, dest1) = points1
        val (source2, dest2) = points2
        displacementV = (
          source1(0) - source2(0),
          source1(1) - source2(1),
          source1(2) - source2(2)
        )

        scannerLoc = (
          dest1(0) - dest2(0),
          dest1(1) - dest2(1),
          dest1(2) - dest2(2),
        )

        if matching.size >= 12 then
          return (matching, displacementV, scannerLoc)

    (matching, displacementV, scannerLoc)
  }

  val ORIENTATIONS = Vector[Tuple3[Int, Int, Int] => Tuple3[Int, Int, Int]](
    (x, y, z) => (x, y, z), // 0
    (x, y, z) => (-x, -y, z),
    (x, y, z) => (-x, y, -z),
    (x, y, z) => (x, -y, -z),
    (x, y, z) => (-x, z, y), // 4
    (x, y, z) => (x, -z, y),
    (x, y, z) => (x, z, -y),
    (x, y, z) => (-x, -z, -y),
    (x, y, z) => (-y, x, z), // 8
    (x, y, z) => (y, -x, z),
    (x, y, z) => (y, x, -z),
    (x, y, z) => (-y, -x, -z),
    (x, y, z) => (y, z, x), // 12
    (x, y, z) => (-y, -z, x),
    (x, y, z) => (-y, z, -x),
    (x, y, z) => (y, -z, -x),
    (x, y, z) => (z, x, y), // 16
    (x, y, z) => (-z, -x, y),
    (x, y, z) => (-z, x, -y),
    (x, y, z) => (z, -x, -y),
    (x, y, z) => (-z, y, x), // 20
    (x, y, z) => (z, -y, x),
    (x, y, z) => (z, y, -x),
    (x, y, z) => (-z, -y, -x)
  )

  def matchWithOrientation(godScanner: Scanner, sc1: Scanner): Option[Tuple3[Scanner, Tuple3[Int, Int, Int], Tuple3[Int, Int, Int]]] = {
    var n = 0
    val orientations = sc1.beacons.par.map((b: Tuple3[Int, Int, Int]) => ORIENTATIONS.map(_(b)))
    while n < 24 do {
      val newScanner = new Scanner(orientations.par.map(_(n)).toVector)
      val (matches, displacement, scannerLoc) = matchBeacons(godScanner, newScanner)
      if matches.size >= 12 then
        return Some((newScanner, displacement, scannerLoc))

        n = 100

      n += 1
    }
    None
  }

  def getBeacons(scanners: Vector[Scanner]): Tuple2[Set[Tuple3[Int, Int, Int]], Vector[Tuple3[Int, Int, Int]]] = {
    var foundScanners = Vector((0, 0, 0))
    var foundScannerIndices = Set(0)
    val points = Set.empty[Tuple3[Int, Int, Int]]
    points.addAll(scanners(0).beacons)

    while foundScanners.size != scanners.size do {
      var godScanner = new Scanner(points.toVector)
      for
        (sc1, i) <- scanners.zipWithIndex
      do
        if !foundScannerIndices.contains(i) then
          matchWithOrientation(godScanner, sc1) match {
            case Some((s, d, scannerLoc)) => {
              foundScanners = foundScanners :+ scannerLoc

              foundScannerIndices.add(i)
              val newBeacons = s.beacons.map((v: Tuple3[Int, Int, Int]) => (v(0) + d(0), v(1) + d(1), v(2) + d(2)))
              points.addAll(newBeacons)
              godScanner.addBeacons(newBeacons)
            }
            case _ =>
          }
        if foundScanners.size == scanners.size then return (points, foundScanners)
    }

    (points, foundScanners)
  }

  def solve(input: Iterator[String]): Tuple2[Int, Int] = {
    var scanners = Vector.empty[Scanner]

    while input.hasNext do {
      var line = input.next()
      if line.startsWith("---") then
        var beacons = Vector.empty[Tuple3[Int, Int, Int]]
        line = input.next()
        while line != "" do {
          val nums = line.split(raw",").map(Integer.parseInt(_))
          beacons = beacons :+ (nums(0), nums(1), nums(2))
          line = if input.hasNext then input.next() else ""
        }
        scanners = scanners :+ new Scanner(beacons)
    }

    val (beacons, scannerLocs) = getBeacons(scanners)

    val maxScannerDist = (for
      (s1Loc, i) <- scannerLocs.zipWithIndex
      (s2Loc, j) <- scannerLocs.zipWithIndex
      if j > i
    yield
      math.abs(s1Loc(0) - s2Loc(0)) + math.abs(s1Loc(1) - s2Loc(1)) + math.abs(s1Loc(2) - s2Loc(2))
    ).max

    (beacons.size, maxScannerDist)
  }

}
