package com.raymond.day10

import com.raymond.helpers.Input

import scala.collection.mutable.Map

object Day10 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day10/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day10/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    var illegalChars = Map[Char, Int]()

    for
      s <- input
    do
      processLine(s) match {
        case Some(c) => illegalChars(c) = illegalChars.getOrElse(c, 0) + 1
        case _ =>  // do nothing
      }

    illegalChars.map((c: Char, n: Int) => c match {
      case ')' => 3 * n
      case ']' => 57 * n
      case '}' => 1197 * n
      case '>' => 25137 * n
    }).sum
  }

  /**
   * Find the illegal character in the given line.
   *
   * @param s line to process
   * @return the illegal character, or None if the line is valid
   */
  def processLine(s: String): Option[Char] = {
    var charStack = List[Char]()
    for
      c <- s
    do
      c match {
        case '(' => charStack = charStack :+ ')'
        case '[' => charStack = charStack :+ ']'
        case '{' => charStack = charStack :+ '}'
        case '<' => charStack = charStack :+ '>'
        case _ => if c == charStack.last then charStack = charStack.dropRight(1) else return Some(c)
      }

    None
  }

  def solve2(input: Iterator[String]): Long = {
    var scores = Vector[Long]()
    for
      s <- input
    do
      processLineWithFinishing(s) match {
        case Some(s) =>  scores = scores :+ computeCompletionScore(s)
        case _ =>  // do nothing
      }

    scores.sortWith((x, y) => x < y)(scores.size / 2)
  }

  /**
   * Complete the given line if the line is incomplete.
   *
   * @param s line to process
   * @return the finishing characters required for this String, or None if the line is corrupted
   */
  def processLineWithFinishing(s: String): Option[String] = {
    var charStack = List[Char]()
    for
      c <- s
    do
      c match {
        case '(' => charStack = charStack :+ ')'
        case '[' => charStack = charStack :+ ']'
        case '{' => charStack = charStack :+ '}'
        case '<' => charStack = charStack :+ '>'
        case _ => if c == charStack.last then charStack = charStack.dropRight(1) else return None
      }

    Some(charStack.reverse.mkString)
  }

  /**
   * Compute the completion score for the given completion String.
   *
   * @param s the completion String
   * @return the score for this completion score
   */
  def computeCompletionScore(s: String): Long = {
    var score = 0L
    for
      c <- s
    do
      score *= 5
      score += (c match {
        case ')' => 1
        case ']' => 2
        case '}' => 3
        case '>' => 4
      })

    score
  }

}
