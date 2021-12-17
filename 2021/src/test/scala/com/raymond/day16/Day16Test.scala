package com.raymond.day16

import org.scalatest.funsuite.AnyFunSuite

class Day16Test extends AnyFunSuite {

  test("Day16.solve1_1") {
    val input = "8A004A801A8002F478".split(raw"\n").iterator

    assert(Day16.solve1(input) == 16)
  }

  test("Day16.solve1_2") {
    val input = "620080001611562C8802118E34".split(raw"\n").iterator

    assert(Day16.solve1(input) == 12)
  }

  test("Day16.solve1_3") {
    val input = "C0015000016115A2E0802F182340".split(raw"\n").iterator

    assert(Day16.solve1(input) == 23)
  }

  test("Day16.solve1_4") {
    val input = "A0016C880162017C3686B18A3D4780".split(raw"\n").iterator

    assert(Day16.solve1(input) == 31)
  }

  test("Day16.parseLiteralPacket") {
    val input = "110100101111111000101000"

    val actual = Day16.parseLiteralPacket(input, "110", "100")
    val expected = (new LiteralPacket(6, 4, 2021), 21)

    assert(actual == expected)
  }

  test("Day16.parseOperatorPacket_1") {
    val input = "00111000000000000110111101000101001010010001001000000000"

    val actual = Day16.parseOperatorPacket(input, "001", "110")
    val expected = (new OperatorPacket(1, 6, Vector(
      new LiteralPacket(6, 4, 10),
      new LiteralPacket(2, 4, 20))), 49
    )

    assert(actual == expected)
  }

  test("Day16.parseOperatorPacket_2") {
    val input = "11101110000000001101010000001100100000100011000001100000"

    val actual = Day16.parseOperatorPacket(input, "111", "011")
    val expected = (new OperatorPacket(7, 3, Vector(
      new LiteralPacket(2, 4, 1),
      new LiteralPacket(4, 4, 2),
      new LiteralPacket(1, 4, 3))), 51
    )

    assert(actual == expected)
  }

  test("Day16.solve2_1") {
    val input = "C200B40A82".split(raw"\n").iterator

    assert(Day16.solve2(input) == 3)
  }

  test("Day16.solve2_2") {
    val input = "04005AC33890".split(raw"\n").iterator

    assert(Day16.solve2(input) == 54)
  }

  test("Day16.solve2_3") {
    val input = "880086C3E88112".split(raw"\n").iterator

    assert(Day16.solve2(input) == 7)
  }

  test("Day16.solve2_4") {
    val input = "CE00C43D881120".split(raw"\n").iterator

    assert(Day16.solve2(input) == 9)
  }

  test("Day16.solve2_5") {
    val input = "D8005AC2A8F0".split(raw"\n").iterator

    assert(Day16.solve2(input) == 1)
  }

  test("Day16.solve2_6") {
    val input = "F600BC2D8F".split(raw"\n").iterator

    assert(Day16.solve2(input) == 0)
  }

  test("Day16.solve2_7") {
    val input = "9C005AC2F8F0".split(raw"\n").iterator

    assert(Day16.solve2(input) == 0)
  }

  test("Day16.solve2_8") {
    val input = "9C0141080250320F1802104A08".split(raw"\n").iterator

    assert(Day16.solve2(input) == 1)
  }

}
