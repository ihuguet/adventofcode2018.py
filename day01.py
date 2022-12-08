#!/usr/bin/env python3

import itertools

with open("day01_in.txt", "r") as f:
    nums = []
    for line in f:
        nums.append(int(line.strip()))

print(f"Part 1: {sum(nums)}")

accum = 0
seen = set([0])
for num in itertools.cycle(nums):
    accum += num
    if accum in seen:
        print(f"Part 2: {accum}")
        break
    seen.add(accum)
