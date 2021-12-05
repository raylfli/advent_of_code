package com.raymond.day4

import com.raymond.helpers.Input

object Day4 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day4/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day4/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): Int = {
    val rawNumbers = input.next().split(raw",")
    val numbers = rawNumbers.map(Integer.parseInt(_))
    input.next() // blank line for separation

    var cards = Vector[BingoCard]()

    while input.hasNext do {
      var line = input.next()
      var nums = Vector[Int]()
      while input.hasNext && line != "" do {
        val split = line.split(raw" ")
        for n <- split if n != "" do nums = nums :+ Integer.parseInt(n.strip())
        line = input.next()
      }
      if !input.hasNext then
        val split = line.split(raw" ")
        for n <- split if n != "" do nums = nums :+ Integer.parseInt(n.strip())
      cards = cards :+ new BingoCard(nums)
    }

    for
      n <- numbers
    do
      for
        card <- cards
      do
        if card.mark(n) then
          return card.getUnmarkedValues().sum * n

    return -1
  }

  def solve2(input: Iterator[String]): Int = {
    val rawNumbers = input.next().split(raw",")
    val numbers = rawNumbers.map(Integer.parseInt(_))
    input.next() // blank line for separation

    var cards = Vector[BingoCard]()

    while input.hasNext do {
      var line = input.next()
      var nums = Vector[Int]()
      while input.hasNext && line != "" do {
        val split = line.split(raw" ")
        for n <- split if n != "" do nums = nums :+ Integer.parseInt(n.strip())
        line = input.next()
      }
      if !input.hasNext then
        val split = line.split(raw" ")
        for n <- split if n != "" do nums = nums :+ Integer.parseInt(n.strip())
      cards = cards :+ new BingoCard(nums)
    }

    val notWonCards = scala.collection.mutable.Set[Int]()
    for
      t <- cards.zipWithIndex
    do
      notWonCards += t(1)

    var last = -1
    for
      n <- numbers
    do
      for
        t <- cards.zipWithIndex
      do
        val card = t(0)
        if !card.won && card.mark(n) then
            notWonCards -= t(1)

      if notWonCards.size == 1 then
        last = notWonCards.toVector(0)

      if notWonCards.size == 0 then
        return cards(last).getUnmarkedValues().sum * n

    return -1
  }

}
