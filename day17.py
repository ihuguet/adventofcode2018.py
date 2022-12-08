#!/usr/bin/env python3

DRAW_RESULT = False  # if true ASCII-draw the result

y_min = x_min = 99999999999
y_max = x_max = 0
rocks = set()
flowed_water = set()
settled_water = set()

with open("day17_in.txt") as f:
    for line in f:
        token1, token2 = line.strip().split(", ")
        vals1 = int(token1[2:])
        vals2 = [int(val) for val in token2[2:].split("..")]
        x_range = [vals1] * 2 if token1[0] == "x" else vals2
        y_range = [vals1] * 2 if token1[0] == "y" else vals2

        x_min = min(x_min, x_range[0])
        x_max = max(x_max, x_range[1])
        y_min = min(y_min, y_range[0])
        y_max = max(y_max, y_range[1])

        for y in range(y_range[0], y_range[1] + 1):
            for x in range(x_range[0], x_range[1] + 1):
                rocks.add((y, x))

LEFT, RIGHT, DOWN, UP = (0, -1), (0, 1), (1, 0), (-1, 0)

def waterfall(pos):
    while pos[0] <= y_max:
        if can_fall(pos):
            mark_flow(pos)
            pos = pos_move(pos, DOWN)
        elif can_flow(pos):
            flow(pos, LEFT)
            flow(pos, RIGHT)
            break # each flow will reach to bottom
        else:
            settle(pos)
            pos = pos_move(pos, UP)

def pos_move(pos, dir):
    return pos[0] + dir[0], pos[1] + dir[1]

def can_fall(pos):
    pos_down = pos_move(pos, DOWN)
    return pos_down not in rocks and pos_down not in settled_water

def can_flow(pos, dir=None):
    if dir != LEFT and dir != RIGHT:
        return can_flow(pos, LEFT) or can_flow(pos, RIGHT) 
    
    while not can_fall(pos) and pos not in rocks:
        pos = pos_move(pos, dir)
    return pos not in rocks

def flow(pos, dir=None):
    if dir != LEFT and dir != RIGHT:
        flow(pos, LEFT)
        flow(pos, RIGHT)
    else:
        while not can_fall(pos) and pos not in rocks:
            mark_flow(pos)
            pos = pos_move(pos, dir)
        if pos not in rocks:
            waterfall(pos)

def mark_flow(pos):
    if pos[0] >= y_min and pos[0] <= y_max:
        flowed_water.add(pos)

def settle(pos, dir=None):
    if dir != LEFT and dir != RIGHT:
        settled_water.add(pos)
        settle(pos, LEFT)
        settle(pos, RIGHT)
    else:
        while (pos := pos_move(pos, dir)) not in rocks:
            settled_water.add(pos)

waterfall((0, 500))
flowed_water.difference_update(settled_water)

if DRAW_RESULT:
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            pos = (y, x)
            if pos in rocks: print('#', end='')
            elif pos in settled_water: print('~', end='')
            elif pos in flowed_water: print('|', end='')
            else: print('.', end='')
        print()

print(f"Part 1: flowed water = {len(flowed_water) + len(settled_water)}")
print(f"Part 2: settled water = {len(settled_water)}")