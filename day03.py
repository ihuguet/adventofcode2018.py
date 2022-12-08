#!/usr/bin/env python3

import re

class Claim:
    def __init__(self, id, x0, y0, x1, y1):
        self.id, self.x0, self.y0, self.x1, self.y1 = id, x0, y0, x1, y1
    
    def __iter__(self):
        def claim_generator(self):
            for x in range(self.x0, self.x1):
                for y in range(self.y0, self.y1):
                    yield (x, y)
        return claim_generator(self)

claims = []
with open("day03_in.txt", "r") as f:
    for line in [l.strip() for l in f]:
        match = re.match("#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)", line)

        id = int(match.group(1))
        x0, y0 = int(match.group(2)), int(match.group(3))
        x1, y1 = x0 + int(match.group(4)), y0 + int(match.group(5))
        claims.append(Claim(id, x0, y0, x1, y1))

claimed = set()
overlap = set()
for claim in claims:
    for point in claim:
        if point in claimed:
            overlap.add(point)
        else:
            claimed.add(point)

print(f"Part 1: points that overlap = {len(overlap)}")

def overlaps(claim):
    for point in claim:
        if point in overlap:
            return True
    return False
    
for claim in claims:
    if not overlaps(claim):
        print(f"Part 2: claim that not overlaps = {claim.id}")
        break