#!/usr/bin/env python3

import re

class XY:
    def __init__(self, x, y):
        self.x, self.y = x, y

class Point:
    def __init__(self, pos, vel):
        self.pos, self.vel = pos, vel

points = []
with open("day10_in.txt", "r") as f:
    for line in f:
        match = re.match(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>", line)
        pos = XY(int(match.group(1)), int(match.group(2)))
        vel = XY(int(match.group(3)), int(match.group(4)))
        points.append(Point(pos, vel))

def minmax(points):
    min = max = None
    for p in points:
        if min is None or p < min:
            min = p
        if max is None or p > max:
            max = p
    return min, max

def print_points(points):
    x_min, x_max = minmax(map(lambda p: p.pos.x, points))
    y_min, y_max = minmax(map(lambda p: p.pos.y, points))
    points = set(map(lambda p: (p.pos.x - x_min, p.pos.y - y_min), points))

    print("-" * 100)
    for y in range(y_max - y_min + 1):
        for x in range(x_max - x_min + 1):
            print("#" if (x, y) in points else " ", end="")
        print()
    print("-" * 100)

second = 0
slow_pass_done = False
while True:
    y_min, y_max = minmax(map(lambda p: p.pos.y, points))
    y_diff = y_max - y_min
    
    if y_diff > 1000:
        step = 100
    elif y_diff > 100:
        step = 10
    else:
        step = 1
    
    second += step
    for p in points:
        p.pos = XY(p.pos.x + step * p.vel.x, p.pos.y + step * p.vel.y)
    
    if y_diff < 40:
        slow_pass_done = True
        print_points(points)
        print(f"second {second}")
        input("Press ENTER...")
    elif slow_pass_done:
        print("Error: you missed the message, please adjust the intervals")
        break

