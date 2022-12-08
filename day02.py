#!/usr/bin/env python3

from collections import Counter

count2 = 0
count3 = 0
with open("day02_in.txt", "r") as f:
    ids = [line.strip() for line in f]

for id in ids:
    has2, has3 = False, False
    letters_counts = Counter(id)
    for count in letters_counts.values():
        if count == 2 and not has2:
            count2 += 1
            has2 = True
        elif count == 3 and not has3:
            count3 += 1
            has3 = True

print(f"Part 1: {count2 * count3}")

def get_similar_substr(id1, id2):
    different_idx = None
    
    for i in range(len(id1)):
        if id1[i] != id2[i]:
            if different_idx == None:
                different_idx = i
            else:
                return None
    
    return id1[:different_idx] + id1[different_idx+1:]

def get_similar_ids(ids):
    for i, id1 in enumerate(ids):
        for id2 in ids[i+1:]:
            if get_similar_substr(id1, id2):
                return (id1, id2)

print(f"Part 2: {get_similar_substr(*get_similar_ids(ids))}")