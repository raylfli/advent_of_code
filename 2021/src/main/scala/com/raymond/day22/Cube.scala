package com.raymond.day22

import scala.math.{max, min}

class Cube(val x1: Int, val x2: Int,
           val y1: Int, val y2: Int,
           val z1: Int, val z2: Int,
           val status: Boolean) {

  val volume: Long = (x2 - x1 + 1).toLong * (y2 - y1 + 1).toLong * (z2 - z1 + 1).toLong * (if status then 1 else -1)

  def intersect(c: Cube): Option[Cube] = {
    val (nx1, nx2,
    ny1, ny2,
    nz1, nz2) = (
      max(x1, c.x1), min(x2, c.x2),
      max(y1, c.y1), min(y2, c.y2),
      max(z1, c.z1), min(z2, c.z2)
    )

    Option(
      if nx1 <= nx2 && ny1 <= ny2 && nz1 <= nz2 then
        new Cube(
          nx1, nx2, ny1, ny2, nz1, nz2, !status
        )
      else
        null
    )
  }

  override def toString: String = s"Cube($status, x1=$x1, x2=$x2, y1=$y1, y2=$y2, z1=$z1, z2=$z2)"

}
