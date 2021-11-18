# Day 16
[Advent of Code - Day 16](https://adventofcode.com/2020/day/16)

# Part 1
The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid ranges of values for each field.

It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only whether tickets contain values that are not valid for any field. 

Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?

# Part 2
Now that you've identified which tickets contain invalid values, discard those tickets entirely. Use the remaining valid tickets to determine which field is which.

Using the valid ranges for each field, determine what order the fields appear on the tickets. The order is consistent between all tickets: if seat is the third field, it is the third field on every ticket, including your ticket.

Once you work out which field is which, look for the six fields on your ticket that start with the word departure. What do you get if you multiply those six values together?
