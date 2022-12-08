#!/usr/bin/env python3

from day16 import op_exec

def run(program, ip_bind, registers):
    ip = registers[ip_bind]

    while ip >= 0 and ip < len(program):
        instr, a, b, c = program[ip]
        registers[ip_bind] = ip
        op_exec(registers, instr, a, b, c)
        ip = registers[ip_bind] + 1

# The program loops for a very long time doing this:
# 
# Before loop start:
# R0 = 0 (at program start R0 = 1, but changes to 0 before the loop)
# R2 = 10551377 (and never changes)
# R5 is IP (instruction pointer) as usual
# 
# Loop:
# ip 3-6:   if R1 * R4 == 10551377:
# ip 7:         R0 += R4
# ip 8:     R1 += 1
# ip 9-10:  if R1 > 10551377:
# ip 12:        R4 += 1
# ip 13-14:     if R4 > 10551377:
# ip 16:            goto END!!!
# ip 15, 2:     R1 = 1
# next ip = 3, repeat loop
#
# This can be simplified even more to this:
def run_part2():
    r0, r4 = 0, 1

    while r4 <= 10551377:
        if 10551377 % r4 == 0:
            r0 += r4
        r4 += 1
    
    return r0

with open("day19_in.txt") as f:
    ip_bind = int(f.readline().split(" ")[1])

    program = []
    for line in f:
        instr, a, b, c = line.strip().split(" ")
        program.append((instr, int(a), int(b), int(c)))

registers = [0] * 6
run(program, ip_bind, registers)
print(f"Part 1: registers[0] = {registers[0]}")
print(f"Part 2: registers[0] = {run_part2()}")

# NOTE:
# to analyze where the program keeps looping, add prints inside `run`, call it
# and stop execution after ~1 minute. Figure out the algorithm to write `run_part2`