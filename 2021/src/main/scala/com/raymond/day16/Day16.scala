package com.raymond.day16

import com.raymond.helpers.Input

object Day16 {
  @main def main = {
    val input1 = Input.getInput("src/main/scala/com/raymond/day16/input.txt")
    println(solve1(input1))

    val input2 = Input.getInput("src/main/scala/com/raymond/day16/input.txt")
    println(solve2(input2))
  }

  def solve1(input: Iterator[String]): BigInt = {
    val transmissionStr = new StringBuilder()
    for
      c <- input.next()
    do {
      transmissionStr ++= String.format("%4s", Integer.parseInt(c.toString, 16).toBinaryString).replace(' ', '0')
    }
    val transmission = transmissionStr.toString
    val (packet, i) = parsePacket(transmission)

    packet.getVersionCodeSum()
  }

  /**
   * Parse one packet from the string and return it and its length
   *
   * @param s binary string that starts with the beginning of a packet
   * @return the Packet and the length of the packet
   */
  def parsePacket(s: String): (Packet, Int) = {
    val version = s.slice(0, 3)
    val tID = s.slice(3, 6)

    if tID == "100" then
      return parseLiteralPacket(s, version, tID)
    else
      return parseOperatorPacket(s, version, tID)
  }

  /**
   * Parse the given literal packet and return a LiteralPacket and the length of the packet.
   *
   * @param s       the packet as a binary string
   * @param version the version code (should match the first three bits of the packet string)
   * @param tID     the type ID (should match bits 3-5 inclusive of the packet string)
   * @return the LiteralPacket and the length of the binary representation
   */
  def parseLiteralPacket(s: String, version: String, tID: String): (Packet, Int) = {
    var i = 6
    val valStr = new StringBuilder()
    valStr += '0'
    while i < s.length && s(i) != '0' do {
      valStr ++= s.slice(i + 1, i + 5)
      i += 5
    }
    valStr ++= s.slice(i + 1, i + 5)
    i += 5
    return (new LiteralPacket(BigInt(version, 2), BigInt(tID, 2), BigInt(valStr.toString(), 2)), i)
  }

  /**
   * Parse the given operator packet and return a OperatorPacket and the length of the packet.
   *
   * @param s       the packet as a binary string
   * @param version the version code (should match the first three bits of the packet string)
   * @param tID     the type ID (should match bits 3-5 inclusive of the packet string)
   * @return the OperatorPacket and the length of the binary representation
   */
  def parseOperatorPacket(s: String, version: String, tID: String): (Packet, Int) = {
    val operatorType = s(6)
    if operatorType == '0' then
      val subPacketLength = Integer.parseInt(s.slice(7, 22), 2)
      var i = 22
      var packets = Vector[Packet]()
      while i < 22 + subPacketLength do {
        val t = parsePacket(s.slice(i, s.length))
        packets = packets :+ t(0)
        i += t(1)
      }
      return (new OperatorPacket(BigInt(version, 2), BigInt(tID, 2), packets), i)
    else
      val numSubPackets = Integer.parseInt(s.slice(7, 18), 2)
      var i = 18
      var packets = Vector[Packet]()
      for
        n <- 0 until numSubPackets
      do
        val t = parsePacket(s.slice(i, s.length))
        packets = packets :+ t(0)
        i += t(1)
      return (new OperatorPacket(BigInt(version, 2), BigInt(tID, 2), packets), i)
  }

  def solve2(input: Iterator[String]): BigInt = {
    val transmissionStr = new StringBuilder()
    for
      c <- input.next()
    do {
      transmissionStr ++= String.format("%4s", Integer.parseInt(c.toString, 16).toBinaryString).replace(' ', '0')
    }
    val transmission = transmissionStr.toString
    val (packet, i) = parsePacket(transmission)

    packet.evaluate()
  }

}
