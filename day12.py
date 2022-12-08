#!/usr/bin/env python3

with open("day12_in.txt") as f:
    state = f.readline().strip().split(" ")[2]
    f.readline()
    changes = {}
    for line in f:
        line = line.strip().split(" => ")
        changes[line[0]] = line[1]

def run(state, generations):
    offset = 0
    seen = {}
    curr_gen = 0
    
    while curr_gen < generations:
        # if the state was already seen, the cycle will repeat forever, advance fast
        if state in seen:
            prev_gen, prev_offset = seen[state]
            gens_jump = curr_gen - prev_gen
            offset_jump = offset - prev_offset
            jumps = (generations - 1 - curr_gen) // gens_jump
            
            curr_gen += gens_jump * jumps
            offset += offset_jump * jumps

            seen.clear() # we're in the final steps, don't have to advance again
        
        seen[state] = curr_gen, offset

        new_state = []
        new_state_len = len(state) + 4

        state = "...." + state + "...."
        for j in range(new_state_len):
            new_state.append(changes[state[j:j + 5]])
        
        new_state = "".join(new_state)
        start = new_state.find("#")
        end = new_state.rfind("#") + 1
        
        state = new_state[start:end]
        offset += 2 - start
        curr_gen += 1

    accum = 0
    for i in range(len(state)):
        if state[i] == "#":
            accum += i - offset
    return accum

print(f"Part 1: sum={run(state, 20)}")
print(f"Part 2: sum={run(state, 50000000000)}")