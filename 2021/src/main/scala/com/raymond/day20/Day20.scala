package com.raymond.day20

import com.raymond.helpers.Input

object Day20 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day20/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day20/input.txt")
    println(solve2(input2))
  }

  def enhanceImage(enhancement: String, image: Set[Tuple2[Long, Long]],
                   topLeft: Tuple2[Long, Long], botRight: Tuple2[Long, Long], invert: Boolean = false): Set[Tuple2[Long, Long]] = {
    var newImage = Set[Tuple2[Long, Long]]()
    for
      x <- topLeft(0) - 1 to botRight(0) + 1
      y <- topLeft(1) - 1 to botRight(1) + 1
    do
      if enhancePixel(enhancement, image, (x, y), topLeft, botRight, invert = invert) == '#' then
        newImage = newImage + Tuple2(x, y)

    newImage
  }

  def enhancePixel(enhancement: String, image: Set[Tuple2[Long, Long]], pixel: Tuple2[Long, Long],
                   topLeft: Tuple2[Long, Long], botRight: Tuple2[Long, Long], invert: Boolean = false): Char = {
    val (x, y) = pixel
    var binNum = 0
    var count = 0
    for
      j <- y - 1 to y + 1
      i <- x - 1 to x + 1
    do
      var on = 0
      if invert then
        on = if i < topLeft(0) || i > botRight(0) || j < topLeft(1) || j > botRight(1) || image.contains((i, j)) then 1 else 0
      else
        on = (if image.contains((i, j)) then 1 else 0)

      binNum += on * math.pow(2, 8 - count).toInt
      count += 1

    enhancement(binNum)
  }

  def printImage(image: Set[Tuple2[Long, Long]], topLeft: Tuple2[Long, Long], botRight: Tuple2[Long, Long]): Unit = {
    for
      y <- topLeft(1) to botRight(1)
    do
      for
        x <- topLeft(0) to botRight(0)
      do
        if image.contains((x, y)) then
          print('#')
        else
          print('.')

      println("")
  }

  def solve1(input: Iterator[String], enhancements: Int = 2): Int = {
    val enhancement = input.next()
    input.next() // blank line

    val doInvert = enhancement(0) == '#' && enhancement(enhancement.length - 1) == '.'
    var invert = false

    var image = Set[Tuple2[Long, Long]]()
    var i = 0
    var j = 0

    while input.hasNext do {
      val line = input.next()
      i = 0
      for
        c <- line
      do
        if c == '#' then
          image = image + Tuple2(i, j)
        i += 1
      j += 1
    }
    var imageL = (0L, 0L) // top left image bound
    var imageR = (i.toLong - 1, j.toLong - 1) // bottom right image bound

    for
      n <- 1 to enhancements
    do
      image = enhanceImage(enhancement, image, imageL, imageR, invert = invert)
      imageL = (imageL(0) - 1, imageL(1) - 1)
      imageR = (imageR(0) + 1, imageR(1) + 1)
      if doInvert then
        invert = !invert

//    printImage(image, imageL, imageR)
    image.size
  }

  def solve2(input: Iterator[String]): Int = {
    solve1(input, enhancements = 50)
  }

}
