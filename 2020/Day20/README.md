# Day 20
[Advent of Code - Day 20](https://adventofcode.com/2020/day/20)

# Part 1
After decoding the satellite messages, you discover that the data actually contains many small images created by the satellite's camera array. The camera array consists of many cameras; rather than produce a single square image, they produce many smaller square image tiles that need to be reassembled back into a single image.

Each camera in the camera array returns a single monochrome image tile with a random unique ID number. The tiles (your puzzle input) arrived in a random order.

Each image tile has been rotated and flipped to a random orientation. Your first task is to reassemble the original image by orienting the tiles so they fit together.

Assemble the tiles into an image. What do you get if you multiply together the IDs of the four corner tiles?

# Part 2
Now, you're ready to search for sea monsters! Because your image is monochrome, a sea monster will look like this:

```
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
```

When looking for this pattern in the image, the spaces can be anything; only the # need to match.

How many # are not part of a sea monster?
