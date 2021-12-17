package com.raymond.day16

abstract class Packet(val version: BigInt, val typeID: BigInt) {

  def evaluate(): BigInt

  def getVersionCodeSum(): BigInt

  override def equals(obj: Any): Boolean = {
    obj match {
      case p: Packet => (version == p.version && typeID == p.typeID)
      case _ => false
    }
  }

}
