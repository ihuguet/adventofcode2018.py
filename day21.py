#!/usr/bin/env python3

from day16 import op_exec

with open("day21_in.txt") as f:
    ip_bind = int(f.readline().split(" ")[1])

    program = []
    for line in f:
        instr, a, b, c = line.strip().split(" ")
        program.append((instr, int(a), int(b), int(c)))

def find_lowest_reg0_init(program, ip_bind):
    registers = [0] * 6
    ip = registers[ip_bind]

    while ip >= 0 and ip < len(program):
        # reg 0 is only used in this instruction. If reg 0 == reg 4, the program halts
        if program[ip] == ('eqrr', 4, 0, 2):
            return registers[4]

        instr, a, b, c = program[ip]
        registers[ip_bind] = ip
        op_exec(registers, instr, a, b, c)
        ip = registers[ip_bind] + 1
    
    return None

def find_highest_reg0_init(program, ip_bind):
    prev_reg4 = reg4 = 0
    seen = set()

    # outer loop
    while True:
        # ip 6-7
        reg3 = reg4 | 65536
        reg4 = 14464005

        # inner 1 loop
        while True:
            # ip 8-12
            reg2 = reg3 & 255
            reg4 += reg2
            reg4 = reg4 & 16777215
            reg4 *= 65899
            reg4 = reg4 & 16777215
            
            # ip 13-14: if 256>reg3 goto 28, else goto 17
            if 256 > reg3:
                # ip 28-30: if reg0==reg4 halt
                if reg4 in seen:  # we're repeating at this point, prev_reg4 was highest possible reg0
                    return prev_reg4
                # else repeat outer loop
                seen.add(reg4)
                prev_reg4 = reg4
                break

            # ip 17: reg2 = 0
            reg2 = 0  # 17: seti 0 _ 2

            # inner 2 loop
            # ip 18-19: reg1 = (reg2 + 1) * 256
            # ip 20-21: if reg1>reg3 goto 26, else goto 24
            #   ip 24-25: reg2++, repeat inner 2 loop
            #   ip 26-27: reg3 = reg2, reg1 = 1, repeat inner 1 loop
            # all these operations can be simplified to:
            reg1 = 256 * (reg3 // 256 + 1)
            reg3 = reg2 = reg1 // 256 - 1
            reg1 = 1

print(f"Part 1: reg 0 init value {find_lowest_reg0_init(program, ip_bind)}")
print(f"Part 2: reg 0 init value {find_highest_reg0_init(program, ip_bind)}")
