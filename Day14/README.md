# Day 14
[Advent of Code - Day 14](https://adventofcode.com/2020/day/14)

# Part 1
The initialization program (your puzzle input) can either update the bitmask or write a value to memory. Values and memory addresses are both 36-bit unsigned integers. For example, ignoring bitmasks for a moment, a line like mem[8] = 11 would write the value 11 to memory address 8.

Execute the initialization program. What is the sum of all values left in memory after it completes? (Do not truncate the sum to 36 bits.)

# Part 2
A version 2 decoder chip doesn't modify the values being written at all. Instead, it acts as a memory address decoder. Immediately before a value is written to memory, each bit in the bitmask modifies the corresponding bit of the destination memory address in the following way:

- If the bitmask bit is *0*, the corresponding memory address bit is unchanged.
- If the bitmask bit is *1*, the corresponding memory address bit is overwritten with 1.
- If the bitmask bit is *X*, the corresponding memory address bit is floating.

A floating bit is not connected to anything and instead fluctuates unpredictably. In practice, this means the floating bits will take on all possible values, potentially causing many memory addresses to be written all at once!

Execute the initialization program using an emulator for a version 2 decoder chip. What is the sum of all values left in memory after it completes?
