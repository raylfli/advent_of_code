package com.raymond.day17

class Projectile(velocityX: Int, velocityY: Int) extends Iterator[Tuple2[Int, Int]] {

  private var (_vx, _vy) = (velocityX, velocityY)
  private var (_x, _y) = (0, 0)

  private var _maxY = 0

  def x = _x
  def y = _y
  def vx = _vx
  def vy = _vy

  def maxY = _maxY

  override def hasNext: Boolean = true

  override def next(): Tuple2[Int, Int] = {
    _x = _x + _vx
    _y = _y + _vy

    _maxY = math.max(_maxY, _y)

    _vx -= math.signum(_vx)
    _vy -= 1

    (_x, _y)
  }

  def dist(p: Tuple2[Int, Int]): Double = {
    math.sqrt(math.pow(p(0) - _x, 2) + math.pow(p(1) - _y, 2))
  }

}
