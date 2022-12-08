#!/usr/bin/env python3

with open("day13_in.txt") as f:
    circuit = [list(l[:-1]) for l in f]

LEFT, UP, RIGHT, DOWN = 0, 1, 2, 3

moves = {
    LEFT:  (0, -1),
    UP:    (-1, 0),
    RIGHT: (0, 1),
    DOWN:  (1, 0)
}

turns = {
    LEFT:  {"/": DOWN,  "\\": UP},
    UP:    {"/": RIGHT, "\\": LEFT},
    RIGHT: {"/": UP,    "\\": DOWN},
    DOWN:  {"/": LEFT,  "\\": RIGHT}
}

class Cart:
    def __init__(self, dir):
        self.dir = dir
        self.step = 0
    
    def turn(self, circuit_segment):
        if circuit_segment in "/\\":
            self.dir = turns[self.dir][circuit_segment]
        elif circuit_segment == "+":
            if self.step == 0:  # left
                self.dir = self.dir - 1 if self.dir > 0 else 3
            elif self.step == 2:  # right
                self.dir = self.dir + 1 if self.dir < 3 else 0
            self.step = self.step + 1 if self.step < 2 else 0

carts = {}
for y, row in enumerate(circuit):
    for x, val in enumerate(row):
        if val in "<>":
            carts[(y, x)] = Cart(LEFT if val == "<" else RIGHT)
            circuit[y][x] = "-"
        elif val in "v^":
            carts[(y, x)] = Cart(DOWN if val == "v" else UP)
            circuit[y][x] = "|"

crashes = []
while len(carts) > 1:
    coords = [pos for pos in carts]
    coords.sort(reverse=True)
    
    while coords:
        pos = coords.pop()
        cart = carts[pos]
        del carts[pos]

        move = moves[cart.dir]
        pos_new = (pos[0] + move[0], pos[1] + move[1])

        # 2 types of collision: -->-<-- and --><--
        if pos_new not in carts:  # no collision (at least yet)
            carts[pos_new] = cart
            cart.turn(circuit[pos_new[0]][pos_new[1]])
        else:  # collision
            del carts[pos_new]
            coords = [p for p in coords if p != pos_new]
            crashes.append(pos_new)

first_crash_pos = crashes[0]
last_cart_pos = list(carts)[0]
print(f"Part 1: pos={first_crash_pos[1]},{first_crash_pos[0]}")
print(f"Part 2: pos={last_cart_pos[1]},{last_cart_pos[0]}")