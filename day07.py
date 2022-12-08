#!/usr/bin/env python3

from collections import OrderedDict

steps = {}
with open("day07_in.txt", "r") as f:
    for line in f:
        words = line.split(" ")
        step, prerequisite = words[7], words[1]
        steps.setdefault(step, set()).add(prerequisite)
        steps.setdefault(prerequisite, set())

done = []
remaining = steps.copy()
while remaining :
    done_set = set(done)
    for step in sorted(remaining):
        prerequisites = remaining[step]
        if prerequisites.issubset(done_set):
            done.append(step)
            del remaining[step]
            break

print(f"Part 1: steps={''.join(done)}")


class Work:
    def __init__(self, step):
        self.step = step
        self.time = 60 + ord(step) - ord('A') + 1

done = set()
remaining = steps
works = []
free_workers = 5
second = 0
while True:
    for step in sorted(remaining):
        if free_workers == 0:
            break
        prerequisites = remaining[step]
        if prerequisites.issubset(done):
            works.append(Work(step))
            free_workers -= 1
            del remaining[step]
    
    if len(remaining) == 0 and len(works) == 0:
        break
    
    second += 1

    for i, work in reversed(list(enumerate(works))):
        work.time -= 1
        if work.time == 0:
            done.add(work.step)
            del works[i]
            free_workers += 1

print(f"Part 2: seconds={second}")