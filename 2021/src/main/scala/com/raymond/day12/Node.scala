package com.raymond.day12

import scala.collection.mutable.Set

class Node(lab: String) {
  val label: String = lab
  val connections: Set[Node] = Set[Node]()
}
