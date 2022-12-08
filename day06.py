#!/usr/bin/env python3

origs = []
with open("day06_in.txt", "r") as f:
    for line in f:
        vals = line.strip().split(", ")
        origs.append((int(vals[0]), int(vals[1])))

def adjacents(point):
    x0, y0 = point
    for x in [x0 - 1, x0, x0 + 1]:
        for y in [y0 - 1, y0, y0 + 1]:
            if x != x0 or y != y0:
                yield (x, y)

def is_infinite(point):
    BORDER_POS = 1000
    return max(abs(point[0]), abs(point[1])) > BORDER_POS

def belongs_to_this_area(point, orig, other_origs):
    orig_dist = calc_distance(point, orig)
    other_dists = [calc_distance(point, other_orig) for other_orig in other_origs]
    return orig_dist < min(other_dists)

def calc_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def sum_all_distances(point, origs):
    return sum(calc_distance(point, orig) for orig in origs)

def calc_area_part1(orig, all_origs):
    area = set([orig])
    other_origs = [o for o in all_origs if o != orig]
    
    queue = list(adjacents(orig))
    while queue:
        point = queue.pop()

        if is_infinite(point):
            return None
        
        if point not in area and belongs_to_this_area(point, orig, other_origs):
            area.add(point)
            queue.extend(adjacents(point))

    return len(area)

def calc_area_part2(origs):
    area = set()

    queue = origs.copy()
    while queue:
        point = queue.pop()
        dists_sum = sum_all_distances(point, origs)

        if dists_sum < 10000 and point not in area:
            area.add(point)
            queue.extend(adjacents(point))
    
    return len(area)

areas = []
for point in origs:
    area = calc_area_part1(point, origs)
    if area is not None:
        areas.append(area)
print(f"Part 1: max area = {max(areas)}")

print(f"Part 2: area = {calc_area_part2(origs)}")
