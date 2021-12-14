package com.raymond.day14

import com.raymond.helpers.Input

import scala.collection.mutable.Map

object Day14 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day14/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day14/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String], steps: Int = 10): Long = {
    val templateChars = input.next().split(raw"")
    val templatePairs = Map[String, Long]() // mapping of pair -> number of occurrences
    for
      i <- 0 until templateChars.length - 1
    do
      val pair = templateChars(i) + templateChars(i + 1)
      templatePairs(pair) = templatePairs.getOrElse(pair, 0L) + 1L

    val lastChar = templateChars(templateChars.size - 1)(0) // need to handle last char separately later

    input.next() // blank line

    val insertionRules = Map[String, String]() // mapping of recognized pair -> inserted string
    while input.hasNext do {
      val mapping = input.next().split(raw" -> ")
      insertionRules(mapping(0)) = mapping(1)
    }

    var pairs = templatePairs // insert over number of steps
    for i <- 1 to steps do {
      pairs = insert(pairs, insertionRules)
    }

    val chars = getNumChars(pairs)
    chars(lastChar) = chars.getOrElse(lastChar, 0L) + 1L // handle last character occurrence

    // get min/max character occurrences
    var minChar = lastChar
    var maxChar = lastChar
    for
      (c, n) <- chars
    do
      if chars(c) < chars(minChar) then
        minChar = c

      if chars(c) > chars(maxChar) then
        maxChar = c


    chars(maxChar) - chars(minChar)
  }

  /**
   * Apply the given rules to the given pairs.
   *
   * @param pairs pairs to apply rules to
   * @param rules rules to apply
   * @return a new Map containing the new pairs
   */
  def insert(pairs: Map[String, Long], rules: Map[String, String]): Map[String, Long] = {
    val newPairs = Map[String, Long]()
    for
      (find, add) <- rules
    do
      val n = pairs.getOrElse(find, 0L)
      if n != 0 then
        newPairs(find(0) + add) = newPairs.getOrElse(find(0) + add, 0L) + n
        newPairs(add + find(1)) = newPairs.getOrElse(add + find(1), 0L) + n

    return newPairs
  }

  /**
   * Compute number of characters given character pairs in the String. The last character of the
   * String will NOT be handled.
   *
   * @param pairs pairs of characters
   * @return the number of occurrences of each character
   */
  def getNumChars(pairs: Map[String, Long]): Map[Char, Long] = {
    val chars = Map[Char, Long]()
    for
      (k, v) <- pairs
    do
      chars(k(0)) = chars.getOrElse(k(0), 0L) + v

    chars
  }

  def solve2(input: Iterator[String]): Long = {
    solve1(input, steps=40)
  }

}
