package com.raymond.day18

import com.raymond.helpers.Input

import java.security.KeyStore.TrustedCertificateEntry
import scala.util.matching.Regex

object Day18 {

  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day18/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day18/input.txt")
    println(solve2(input2))
  }

  /**
   * Construct the tree representing this snailfish number.
   *
   * @param s the snailfish number String
   * @return the root Node
   */
  def constructTree(s: String): Node = {
    if s(0).isDigit then
      new Number(Integer.parseInt(s))
    else
      val strippedString = s.slice(1, s.length - 1)
      var bracketCount = 0
      var i = 0
      if !strippedString(0).isDigit then {
        bracketCount += 1
        i += 1
      }

      while bracketCount != 0 || strippedString(i).isDigit do {
        strippedString(i) match {
          case '[' => bracketCount += 1
          case ']' => bracketCount -= 1
          case _ =>
        }
        i += 1
      }
      val l = constructTree(strippedString.slice(0, i))
      val r = constructTree(strippedString.slice(i + 1, strippedString.length))

      new Pair(l, r)
  }

  /**
   * Reduce the given tree if possible.
   *
   * @param root root of the tree
   * @return reduced root of the tree
   */
  def reduce(root: Node): Node = {
    var res = root
    var reduced = true
    while reduced do {
      val expRes = explode(res)
      res = expRes(0)
      reduced = expRes(1)
      if !reduced then
        val splRes = split(res)
        res = splRes(0)
        reduced = splRes(1)
    }
    res
  }

  /**
   * Explode the given tree.
   *
   * @param root root of the tree
   * @param depth depth of recursion (first execution should use depth=0)
   * @return the root of the exploded tree
   */
  def explode(root: Node, depth: Int = 0): Tuple4[Node, Boolean, Node, Node] = {
    root match {
      case p: Pair => {
        var (l, r) = (p.left, p.right)
        if depth >= 4 then
          return (new Number(0), true, l, r)
        else
          val expRes = explode(l, depth=depth + 1)
          l = expRes(0)
          var reduced = expRes(1)
          var expL = expRes(2)
          var expR = expRes(3)
          if reduced then
            expR match {
              case num: Number if num.n != 0 => {
                r = addLeft(r, expR)
                expR = new Number(0)
              }
              case _ =>
            }
          else
            val expRes = explode(r, depth=depth + 1)
            r = expRes(0)
            reduced = expRes(1)
            expL = expRes(2)
            expR = expRes(3)
            if reduced then
              expL match {
                case num: Number if num.n != 0 => {
                  l = addRight(l, expL)
                  expL = new Number(0)
                }
                case _ =>
              }
          if reduced then
            return (new Pair(l, r), true, expL, expR)
      }
      case n: Number => return (root, false, new Number(0), new Number(0))
    }

    (root, false, new Number(0), new Number(0))
  }

  /**
   * Add on the left side of a tree.
   *
   * @param root root of the tree
   * @param other other node to add
   * @return
   */
  def addLeft(root: Node, other: Node): Node = {
    root match {
      case num: Number => {
        return new Number(num.n + other.asInstanceOf[Number].n)
      }
      case p: Pair => {
        var (a, b) = (p.left, p.right)
        return new Pair(addLeft(a, other), b)
      }
    }
  }

  /**
   * Add on the right side of a tree.
   *
   * @param root root of the tree
   * @param other other node to add
   * @return
   */
  def addRight(root: Node, other: Node): Node = {
    root match {
      case num: Number => {
        return new Number(num.n + other.asInstanceOf[Number].n)
      }
      case p: Pair => {
        var (a, b) = (p.left, p.right)
        return new Pair(a, addRight(b, other))
      }
    }
  }

  /**
   * Split the given tree.
   *
   * @param root root of the tree
   * @return the root of the split ree
   */
  def split(root: Node): Tuple2[Node, Boolean] = {
    root match {
      case num: Number => {
        if num.n >= 10 then {
          val x = num.n / 2
          return (new Pair(new Number(x), new Number(num.n - x)), true)
        }
      }

      case p: Pair => {
        var (l, r) = (p.left, p.right)
        var reduced = false
        val splitRes = split(l)
        l = splitRes(0)
        reduced = splitRes(1)
        if !reduced then
          val splitRes2 = split(r)
          r = splitRes2(0)
          reduced = splitRes2(1)

        if reduced then
          return (new Pair(l, r), true)
      }
    }

    (root, false)
  }

  def solve1(input: Iterator[String]): Int = {
    val treeInp = input.map(constructTree(_))

    var res = treeInp.next()
    while treeInp.hasNext do {
      val newPair = new Pair(res, treeInp.next())
      res = reduce(newPair)
    }

    res.magnitude()
  }


  def solve2(input: Iterator[String]): Int = {
    val trees = input.map(constructTree(_)).toVector

    var maxMag = 0
    for
      (t1, i) <- trees.zipWithIndex
      (t2, j) <- trees.zipWithIndex
      if i != j
    do
      val pair1 = new Pair(t1, t2)
      val pair2 = new Pair(t2, t1)

      val res1 = reduce(pair1)
      val res2 = reduce(pair2)

      val resMaxMag = math.max(res1.magnitude(), res2.magnitude())

      maxMag = math.max(maxMag, resMaxMag)

    maxMag
  }

}
