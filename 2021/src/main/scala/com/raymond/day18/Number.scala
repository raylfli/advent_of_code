package com.raymond.day18

class Number(initNumber: Int) extends Node {

  var n = initNumber

  override def equals(obj: Any): Boolean = {
    obj match {
      case node: Number => n == node.n
      case _ => false
    }
  }

  override def toString: String = n.toString

  override def magnitude(): Int = n

}
