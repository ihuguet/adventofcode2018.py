#!/usr/bin/env python3

INPUT = "360781"

input_int = int(INPUT)
input_arr = [int(d) for d in INPUT]

pos1, pos2 = 0, 1
recipes = [3, 7]

part2_result = None
while part2_result is None or len(recipes) < input_int  + 10:
    val1, val2 = recipes[pos1], recipes[pos2]
    
    new_val = val1 + val2
    if new_val > 9:
        recipes.extend([new_val // 10, new_val % 10])
    else:
        recipes.append(new_val)
    
    pos1 = (pos1 + val1 + 1) % len(recipes)
    pos2 = (pos2 + val2 + 1) % len(recipes)

    if part2_result is None:
        if recipes[-6:] == input_arr:
            part2_result = len(recipes) - 6
        elif recipes[-7:-1] == input_arr:
            part2_result = len(recipes) - 7

part1_result = ''.join(str(n) for n in recipes[input_int:input_int + 11])
print(f"Part 1: {part1_result}")
print(f"Part 2: {part2_result}")
