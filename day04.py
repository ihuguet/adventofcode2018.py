#!/usr/bin/env python3

class GuardSleeps:
    def __init__(self, id):
        self.id = id
        self.total = 0
        self.by_minute = [0] * 60
    
    def add_sleep_period(self, start, end):
        self.total += end - start
        for m in range(start, end):
            self.by_minute[m] += 1

with open("day04_in.txt", "r") as f:
    lines = [l.strip() for l in f]

lines.sort()

guard = None
sleep_start = None
guard_max = GuardSleeps(-1)
guards = {}
for line in lines:
    date = line[1:11]
    hour = line[12:14]
    minute = int(line[15:17]) - (60 if hour == "23" else 0)
    action = line[19:]

    if action == "falls asleep":
        if sleep_start != None:
            raise Exception(f"Unordered sleep event at date {date}")
        sleep_start = minute
    elif action == "wakes up":
        if sleep_start == None:
            raise Exception(f"Unordered wake event at date {date}")
        guard.add_sleep_period(sleep_start, minute)
        sleep_start = None
    else: # guard begins shift        
        guard_id = int(action[7:].split(" ")[0])
        if guard_id not in guards:
            guards[guard_id] = GuardSleeps(guard_id)
        guard = guards[guard_id]

    if guard.total > guard_max.total:
        guard_max = guard

minute_max = -1
count_max = -1
for i, count in enumerate(guard_max.by_minute):
    if count > count_max:
        minute_max = i
        count_max = count

print(f"Part 1: guard {guard_max.id} x minute {minute_max} = {guard_max.id * minute_max}")

minute_max = -1
count_max = -1
for m in range(0, 60):
    for guard in guards.values():
        count = guard.by_minute[m]
        if count > count_max:
            guard_max = guard
            minute_max = m
            count_max = count

print(f"Part 2: guard {guard_max.id} x minute {minute_max} = {guard_max.id * minute_max}")