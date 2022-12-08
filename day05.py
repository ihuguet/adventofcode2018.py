#!/usr/bin/env python3

with open("day05_in.txt", "r") as f:
    polymer = f.read().strip()

def reacts(elem1, elem2):
    return elem1 != elem2 and elem1.lower() == elem2.lower()

def reduce_polymer(polymer_in, discard_elem=None):
    discard = lambda elem: elem.lower() != discard_elem

    polymer_out = []
    for elem in filter(discard, polymer_in):
        if len(polymer_out) > 0 and reacts(polymer_out[-1], elem):
            polymer_out.pop()
        else:
            polymer_out.append(elem)
    
    return polymer_out

min_len = len(reduce_polymer(polymer))
print(f"Part 1: result polymer len = {min_len}")

all_elems = (chr(n) for n in range(ord("a"), ord("z") + 1))
min_len = min(len(reduce_polymer(polymer, elem)) for elem in all_elems)
print(f"Part 2: min result polymer len = {min_len}")