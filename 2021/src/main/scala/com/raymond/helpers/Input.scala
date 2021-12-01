package com.raymond.helpers

object Input {

  def getInput(filePath: String) = {
    val source = scala.io.Source.fromFile(filePath)
    source.getLines().iterator
  }

}
