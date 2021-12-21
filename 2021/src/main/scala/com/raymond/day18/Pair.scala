package com.raymond.day18

class Pair(l: Node, r: Node) extends Node {

  var left = l
  var right = r

  override def equals(obj: Any): Boolean = {
    obj match {
      case n: Pair => left == n.left && right == n.right
      case _ => false
    }
  }

  override def toString: String = '[' + left.toString + ',' + right.toString + ']'

  override def magnitude(): Int = 3 * left.magnitude() + 2 * right.magnitude()

}
