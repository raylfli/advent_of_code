package com.raymond.day21

abstract class Die extends Iterator[Int] {

  protected var _totalNumRolls = 0

  def totalNumRolls = _totalNumRolls

  override def hasNext: Boolean = true

}
