# Day 8
[Advent of Code - Day 8](https://adventofcode.com/2020/day/8)

# Part 1
The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).

Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?

# Part 2
The program is supposed to terminate by attempting to execute an instruction immediately after the last instruction in the file. By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.

Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?
