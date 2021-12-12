package com.raymond.day12

import com.raymond.helpers.Input

object Day12 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day12/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day12/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    val startNode = new Node("start")
    val nodes = scala.collection.mutable.Map[String, Node]("start" -> startNode)  // node label -> node

    for
      row <- input
    do
      val connection = row.split(raw"-")
      val nodeA = nodes.getOrElse(connection(0), new Node(connection(0)))
      val nodeB = nodes.getOrElse(connection(1), new Node(connection(1)))

      nodeA.connections.add(nodeB)
      nodeB.connections.add(nodeA)

      nodes.addOne(nodeA.label, nodeA)
      nodes.addOne(nodeB.label, nodeB)

    numPaths(startNode, nodes)
  }

  /**
   * Recursively compute the number of paths.
   *
   * @param root root to compute paths from
   * @param nodes mapping of node labels to nodes
   * @return the number of paths
   */
  def numPaths(root: Node, nodes: scala.collection.mutable.Map[String, Node]): Int = {
    _numPaths(root, nodes, Set[String]())
  }

  /**
   * Recursively compute the number of paths.
   *
   * @param root root to compute paths from
   * @param nodes mapping of node labels to nodes
   * @param visited labels of nodes visited and the number of visits
   * @return the number of paths
   */
  private def _numPaths(root: Node, nodes: scala.collection.mutable.Map[String, Node], visited: Set[String]): Int = {
    if root.label == "end" then
      return 1
    else if visited.contains(root.label) then
      return 0

    var nowVisited = visited
    if !root.label(0).isUpper then
      nowVisited = visited + root.label

    var paths = 0
    for
      node <- root.connections
    do
      paths += _numPaths(node, nodes, nowVisited)

    paths
  }

  def solve2(input: Iterator[String]): Int = {
    val startNode = new Node("start")
    val nodes = scala.collection.mutable.Map[String, Node]("start" -> startNode)  // node label -> node

    for
      row <- input
    do
      val connection = row.split(raw"-")
      val nodeA = nodes.getOrElse(connection(0), new Node(connection(0)))
      val nodeB = nodes.getOrElse(connection(1), new Node(connection(1)))

      nodeA.connections.add(nodeB)
      nodeB.connections.add(nodeA)

      nodes.addOne(nodeA.label, nodeA)
      nodes.addOne(nodeB.label, nodeB)

    numPathsDoubleVisit(startNode, nodes)
  }

  /**
   * Recursively compute the number of paths.
   *
   * @param root root to compute paths from
   * @param nodes mapping of node labels to nodes
   * @return the number of paths
   */
  def numPathsDoubleVisit(root: Node, nodes: scala.collection.mutable.Map[String, Node]): Int = {
    (for
      node <- root.connections
    yield
      _numPathsDoubleVisit(node, nodes, Set[String](root.label))).sum
  }

  /**
   * Recursively compute the number of paths.
   *
   * @param root root to compute paths from
   * @param nodes mapping of node labels to nodes
   * @param visited labels of nodes visited and the number of visits
   * @param doubleVisit whether a double visit of a small cave has already happened
   * @return the number of paths
   */
  private def _numPathsDoubleVisit(root: Node, nodes: scala.collection.mutable.Map[String, Node], visited: Set[String], doubleVisit: Boolean = false): Int = {
    var nowDoubleVisit = doubleVisit
    if root.label == "end" then
      return 1
    else if visited.contains(root.label) && doubleVisit || root.label == "start" then
      return 0
    else if visited.contains(root.label) && !doubleVisit && root.label(0).isLower then
      nowDoubleVisit = true

    var nowVisited = visited
    if !root.label(0).isUpper then
      nowVisited = visited + root.label

    var paths = 0
    for
      node <- root.connections
    do
      paths += _numPathsDoubleVisit(node, nodes, nowVisited, doubleVisit=nowDoubleVisit)

    paths
  }

}
