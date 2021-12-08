package com.raymond.day8

import com.raymond.helpers.Input

import scala.collection.mutable.Map
import scala.collection.mutable.Set

object Day8 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day8/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day8/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    val entries = input.map(_.split(raw"\|"))
    val values = entries.map(_(1).strip().split(raw" "))

    var count = 0
    for
      value <- values
    do
      for
        num <- value
      do
        count += (num.strip().length match {
          case 2 | 4 | 3 | 7 => 1
          case _ => 0
        })

    count
  }

  def solve2(input: Iterator[String]): Int = {
    val entries = input.map(_.split(raw"\|")).toVector
    val patterns = entries.map(_(0).strip().split(raw" "))
    val values = entries.map(_(1).strip().split(raw" ")).toVector

    val decoders = patterns.map(new Decoder(_))

    var sum = 0
    for
      t <- decoders.zipWithIndex
    do
      val decoder = t(0)
      val vals = values(t(1)).map(decoder.decode(_))
      sum += vals(0) * 1000 + vals(1) * 100 + vals(2) * 10 + vals(3)
    sum
  }

}
