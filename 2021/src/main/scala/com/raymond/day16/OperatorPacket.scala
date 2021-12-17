package com.raymond.day16

class OperatorPacket(version: BigInt, typeID: BigInt, initSubPackets: Vector[Packet]) extends Packet(version, typeID) {

  val subPackets = initSubPackets

  override def evaluate(): BigInt = {
    typeID match {
      case 0 => subPackets.map(_.evaluate()).sum
      case 1 => subPackets.map(_.evaluate()).product
      case 2 => subPackets.map(_.evaluate()).min
      case 3 => subPackets.map(_.evaluate()).max
      case 5 => checkBool(subPackets(0).evaluate() > subPackets(1).evaluate())
      case 6 => checkBool(subPackets(0).evaluate() < subPackets(1).evaluate())
      case 7 => checkBool(subPackets(0).evaluate() == subPackets(1).evaluate())
    }
  }

  private def checkBool(b: Boolean) = if b then 1 else 0

  override def getVersionCodeSum(): BigInt = {
    version + subPackets.map(_.getVersionCodeSum()).sum
  }

  override def equals(obj: Any): Boolean = {
    obj match {
      case o: OperatorPacket => (version == o.version && typeID == o.typeID && subPackets.equals(o.subPackets))
      case _ => false
    }
  }

}
