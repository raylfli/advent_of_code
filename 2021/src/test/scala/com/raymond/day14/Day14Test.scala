package com.raymond.day14

import org.scalatest.funsuite.AnyFunSuite

import scala.collection.mutable.Map

class Day14Test extends AnyFunSuite {

  val puzzleInput = "NNCB\n\nCH -> B\nHH -> N\nCB -> H\nNH -> C\nHB -> C\nHC -> B\nHN -> C\nNN -> C\nBH -> H\nNC -> B\nNB -> B\nBN -> B\nBB -> N\nBC -> B\nCC -> N\nCN -> C"

  test("Day14.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day14.solve1(input) == 1588)
  }

  test("Day14.insert") {
    val pairs = Map[String, Long]("NN" -> 1, "NC" -> 1, "CB" -> 1)
    val rules = Map[String, String]("CH" -> "B", "HH" -> "N", "CB" -> "H", "NH" -> "C", "HB" -> "C", "HC" -> "B", "HN" -> "C", "NN" -> "C", "BH" -> "H", "NC" -> "B", "NB" -> "B", "BN" -> "B", "BB" -> "N", "BC" -> "B", "CC" -> "N", "CN" -> "C")

    val newPairs = Day14.insert(pairs, rules)
    val expected = Map[String, Long]("NC" -> 1, "CN" -> 1, "NB" -> 1, "BC" -> 1, "CH" -> 1, "HB" -> 1)
    for
      (k, v) <- expected
    do
      assert(newPairs(k) == v)
//    assert(Day14.insert(pairs, rules) == Map[String, Int]("NC" -> 1, "CN" -> 1, "NB" -> 1, "BC" -> 1, "CH" -> 1, "HB" -> 1))
  }

  test("Day14.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day14.solve2(input) == 2188189693529L)
  }

}
