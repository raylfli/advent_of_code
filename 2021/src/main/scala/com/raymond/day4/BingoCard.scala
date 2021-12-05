package com.raymond.day4

class BingoCard(val nums: Vector[Int]) {
  var _unmarked = scala.collection.mutable.Set[Int](
    0, 1, 2, 3, 4, 5,
    6, 7, 8, 9, 10,
    11, 12, 13, 14, 15,
    16, 17, 18, 19, 20,
    21, 22, 23, 24)  // indices of unmarked numbers
  private var _values = scala.collection.mutable.Map[Int, Int]()  // mapping of values to indices
  private var _indices = scala.collection.mutable.Map[Int, Int]()  // mapping of indices to values

  private var _won = false
  val won = _won

  for
    t <- nums.zipWithIndex
  do
    _values(t(0)) = t(1)
    _indices(t(1)) = t(0)

  def mark(num: Int): Boolean = {
    val i = _values.get(num)

    i match {
      case None => return false
      case Some(i) => {
        _unmarked -= i
        return checkWin()
      }
      case _ => return false
    }
    return false
  }

  def checkWin(): Boolean = {
    for
      r <- 0 to 4
    do
      if checkRow(r) then
        _won = true
        return true

    for
      c <- 0 to 4
    do
      if checkCol(c) then
        _won = true
        return true

    return false
  }

  def checkRow(r: Int): Boolean = {
    for
      i <- r * 5 until r * 5 + 5
    do
      if _unmarked.contains(i) then
        return false

    return true
  }

  def checkCol(c: Int): Boolean = {
    for
      i <- 0 until 5
    do
      if _unmarked.contains(i * 5 + c) then
        return false

    return true
  }

  def getUnmarkedValues(): Vector[Int] = {
    _unmarked.map(_indices.get(_).getOrElse(-1)).toVector
  }
}
