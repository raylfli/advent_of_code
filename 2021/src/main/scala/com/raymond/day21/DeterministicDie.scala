package com.raymond.day21

class DeterministicDie extends Die {

  private var n = 0

  override def next(): Int = {
    _totalNumRolls += 1
    n = (n + 1) % 100
    n
  }
}
