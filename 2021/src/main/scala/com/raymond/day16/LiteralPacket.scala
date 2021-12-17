package com.raymond.day16

class LiteralPacket(version: BigInt, typeID: BigInt, val value: BigInt) extends Packet(version, typeID) {

  private val n = value

  override def evaluate(): BigInt = n

  override def getVersionCodeSum(): BigInt = version

  override def equals(obj: Any): Boolean = {
    obj match {
      case l: LiteralPacket => (value == l.value && version == l.version && typeID == l.typeID)
      case _ => false
    }
  }
}
