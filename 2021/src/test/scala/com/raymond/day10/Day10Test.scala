package com.raymond.day10

import org.scalatest.funsuite.AnyFunSuite

class Day10Test extends AnyFunSuite {

  val puzzleInput = "[({(<(())[]>[[{[]{<()<>>\n[(()[<>])]({[<{<<[]>>(\n{([(<{}[<>[]}>{[]{[(<()>\n(((({<>}<{<{<>}{[]{[]{}\n[[<[([]))<([[{}[[()]]]\n[{[{({}]{}}([{[{{{}}([]\n{<[[]]>}<{[{[{[]{()[[[]\n[<(<(<(<{}))><([]([]()\n<{([([[(<>()){}]>(<<{{\n<{([{{}}[<[[[<>{}]]]>[]]"

  test("Day10.solve1") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day10.solve1(input) == 26397)
  }

  test("Day10.processLine") {
    val input = "{([(<{}[<>[]}>{[]{[(<()>"
    val result = Day10.processLine(input)
    result match {
      case Some(c) => assert(c == '}')
      case _ => fail("Line is corrupted but processing returned no corruption")
    }
  }

  test("Day10.processLine2") {
    val input = "[[<[([]))<([[{}[[()]]]"
    val result = Day10.processLine(input)
    result match {
      case Some(c) => assert(c == ')')
      case _ => fail("Line is corrupted but processing returned no corruption")
    }
  }

  test("Day10.processLine3") {
    val input = "[{[{({}]{}}([{[{{{}}([]"
    val result = Day10.processLine(input)
    result match {
      case Some(c) => assert(c == ']')
      case _ => fail("Line is corrupted but processing returned no corruption")
    }
  }

  test("Day10.processLine4") {
    val input = "[<(<(<(<{}))><([]([]()"
    val result = Day10.processLine(input)
    result match {
      case Some(c) => assert(c == ')')
      case _ => fail("Line is corrupted but processing returned no corruption")
    }
  }

  test("Day10.processLine5") {
    val input = "<{([([[(<>()){}]>(<<{{"
    val result = Day10.processLine(input)
    result match {
      case Some(c) => assert(c == '>')
      case _ => fail("Line is corrupted but processing returned no corruption")
    }
  }

  test("Day10.processLineValid") {
    val input = "[<>({}){}[([])<>]]"
    val result = Day10.processLine(input)
    result match {
      case Some(c) => fail("Line is valid but found to be invalid")
      case _ => assert(true)
    }
  }

  test("Day10.solve2") {
    val input = puzzleInput.split(raw"\n").iterator

    assert(Day10.solve2(input) == 288957)
  }

  test("Day10.processLineWithFinishing") {
    val input = "[({(<(())[]>[[{[]{<()<>>"
    val result = Day10.processLineWithFinishing(input)
    result match {
      case Some(s) => assert(s == "}}]])})]")
      case _ => fail("Line is incomplete but processing returned corruption")
    }
  }

  test("Day10.processLineWithFinishing2") {
    val input = "[(()[<>])]({[<{<<[]>>("
    val result = Day10.processLineWithFinishing(input)
    result match {
      case Some(s) => assert(s == ")}>]})")
      case _ => fail("Line is incomplete but processing returned corruption")
    }
  }

  test("Day10.processLineWithFinishing3") {
    val input = "(((({<>}<{<{<>}{[]{[]{}"
    val result = Day10.processLineWithFinishing(input)
    result match {
      case Some(s) => assert(s == "}}>}>))))")
      case _ => fail("Line is incomplete but processing returned corruption")
    }
  }

  test("Day10.processLineWithFinishing4") {
    val input = "{<[[]]>}<{[{[{[]{()[[[]"
    val result = Day10.processLineWithFinishing(input)
    result match {
      case Some(s) => assert(s == "]]}}]}]}>")
      case _ => fail("Line is incomplete but processing returned corruption")
    }
  }

  test("Day10.processLineWithFinishing5") {
    val input = "<{([{{}}[<[[[<>{}]]]>[]]"
    val result = Day10.processLineWithFinishing(input)
    result match {
      case Some(s) => assert(s == "])}>")
      case _ => fail("Line is incomplete but processing returned corruption")
    }
  }

  test("Day10.computeCompletionScore") {
    val input = "}}]])})]"
    assert(Day10.computeCompletionScore(input) == 288957)
  }

  test("Day10.computeCompletionScore2") {
    val input = ")}>]})"
    assert(Day10.computeCompletionScore(input) == 5566)
  }

  test("Day10.computeCompletionScore3") {
    val input = "}}>}>))))"
    assert(Day10.computeCompletionScore(input) == 1480781)
  }

  test("Day10.computeCompletionScore4") {
    val input = "]]}}]}]}>"
    assert(Day10.computeCompletionScore(input) == 995444)
  }

  test("Day10.computeCompletionScore5") {
    val input = "])}>"
    assert(Day10.computeCompletionScore(input) == 294)
  }

}
