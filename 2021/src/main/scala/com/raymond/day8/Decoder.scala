package com.raymond.day8


class Decoder(patterns: Iterable[String]) {

  private val wiresToSegments = unscrambleWires(patterns)
  private val segmentsToNumbers = Map[Set[Int], Int](  // omitting easy cases of 1, 4, 7, 8
    Set(0, 1, 2, 4, 5, 6) -> 0,
    Set(0, 2, 3, 4, 6) -> 2,
    Set(0, 2, 3, 5, 6) -> 3,
    Set(0, 1, 3, 5, 6) -> 5,
    Set(0, 1, 3, 4, 5, 6) -> 6,
    Set(0, 1, 2, 3, 5, 6) -> 9
  )

  private def unscrambleWires(patterns: Iterable[String]): Map[String, Int] = {
    val patts = patterns
      .toVector
      .sortWith((a, b) => a.length() < b.length())
      .map((x: String) => Set.from(x.split(raw"")))

    val one = patts(0)
    val seven = patts(1)

    // wire inputs to segment indices
    // first, 7 has one more segment than 1 (segment 0)
    val segmentZero = (seven -- one).toVector(0)
    var segments = Map[String, Int](segmentZero -> 0) // segment 0

    // patts.slice(3, 6) are the patterns containg the numbers 2, 3, 5
    val twoThreeFive = patts.slice(3, 6)

    // 3 shares 2 segments w/ 1 (segments 2, 5)
    var three = Set[String]()
    var threeIndex = 0
    for
      check <- twoThreeFive.zipWithIndex
    do
      if (check(0) & one) == one then
        three = check(0)
        threeIndex = check(1)

    // intersection of 3 and 4 share three segments: 2, 3, 5
    // if we set minus with the segments in 1, we get segment 3
    val four = patts(2)
    val threeAndFour = three & four
    segments = segments + ((threeAndFour -- one).toVector(0) -> 3)

    // set minus of 4 minus the intersection of 3 and 4 gives segment 1
    segments = segments + ((four -- threeAndFour).toVector(0) -> 1)

    // set minus of 3 - 4 - segment 0 is segment 6
    segments = segments + (((three -- four) - segmentZero).toVector(0) -> 6)

    // for the number 5, intersection of it and 3 should share 3 segments
    var five = Set[String]()
    for
      check <- twoThreeFive.zipWithIndex
    do
      if check(1) != threeIndex && (check(0) & four).size == 3 then
        five = check(0)

    // then, segment 5 is intersection of 5 and 1
    val fiveAndOne = five & one
    segments = segments + (fiveAndOne.toVector(0) -> 5)

    // segment 2 is set minus of 1 minus intersection of 5 and 1
    segments = segments + ((one -- fiveAndOne).toVector(0) -> 2)

    // finally, segment 4 is segminus of 8 minus all segments already captured
    segments = segments + ((patts(9) -- segments.keySet).toVector(0) -> 4)

    segments
  }

  def decode(chars: String): Int = {
    val segments = chars.split(raw"").map(wiresToSegments(_)).toSet

    segments.size match {
      case 2 => 1
      case 3 => 7
      case 4 => 4
      case 7 => 8
      case _ => segmentsToNumbers(segments)
    }
  }
}
