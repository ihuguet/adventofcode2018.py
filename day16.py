#!/usr/bin/env python3

def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def band(a, b):
    return a & b

def bor(a, b):
    return a | b

def mov(a, b):
    return a

def gt(a, b):
    return 1 if a > b else 0

def eq(a, b):
    return 1 if a == b else 0

def op_exec(registers, op_name, a, b, c):
    type_a, type_b, fn = operations[op_name]

    if type_a == REG:
        a = registers[a]
    if type_b == REG:
        b = registers[b]

    registers[c] = fn(a, b)

REG, IMM = 0, 1
operations = {
    'addr': (REG, REG, add),
    'addi': (REG, IMM, add),
    'mulr': (REG, REG, mul),
    'muli': (REG, IMM, mul),
    'banr': (REG, REG, band),
    'bani': (REG, IMM, band),
    'borr': (REG, REG, bor),
    'bori': (REG, IMM, bor),
    'setr': (REG, IMM, mov),
    'seti': (IMM, IMM, mov),
    'gtir': (IMM, REG, gt),
    'gtri': (REG, IMM, gt),
    'gtrr': (REG, REG, gt),
    'eqir': (IMM, REG, eq),
    'eqri': (REG, IMM, eq),
    'eqrr': (REG, REG, eq)
}

if __name__ == "__main__":  # avoid executing if we're importing from day19

    # read file
    with open("day16_in.txt") as f:
        lines = f.readlines()

    # read part 1
    samples = []
    line_idx = 0
    while True:
        lines_sample = [l.strip() for l in lines[line_idx:line_idx + 3]]

        if lines_sample[0] == "":
            break

        before = [int(val) for val in lines_sample[0][9:-1].split(", ")]
        instruction = [int(val) for val in lines_sample[1].split(" ")]
        after = [int(val) for val in lines_sample[2][9:-1].split(", ")]
        samples.append((instruction, before, after))

        line_idx += 4

    # read part 2
    lines_part2 = lines[line_idx + 2:]
    program = [[int(val) for val in line.strip().split(" ")] for line in lines_part2]

    # use the samples to discard as much as op_code->op_name mappings as possible
    match_x3_count = 0
    names_all = set(op_name for op_name in operations)
    ops_map = {opcode: names_all.copy() for opcode in range(16)}

    for (opcode, a, b, c), before, after in samples:
        match_ops = set()

        for op_name in operations:
            registers = before.copy()
            op_exec(registers, op_name, a, b, c)
            if registers == after:
                match_ops.add(op_name)
        
        ops_map[opcode].intersection_update(match_ops)

        if len(match_ops) >= 3:
            match_x3_count += 1

    print(f"Part 1: count = {match_x3_count}")

    # the opcodes mapped to a singe op_name can be used to discard that name for
    # other opcodes, repeating until all mappings are resolved to a single name
    names_resolved = set()
    while len(names_resolved) < 15:
        names_resolved = set(next(iter(names)) for names in ops_map.values() if len(names) == 1)
        for names in ops_map.values():
            if len(names) > 1:
                names.difference_update(names_resolved)

    ops_map = {opcode: next(iter(names)) for opcode, names in ops_map.items()}

    # run program (part 2)
    registers = [0] * 4
    for opcode, a, b, c in program:
        op_exec(registers, ops_map[opcode], a, b, c)

    print(f"Part 2: registers[0] = {registers[0]}")