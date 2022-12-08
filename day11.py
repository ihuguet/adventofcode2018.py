#!/usr/bin/env python3

INPUT = 9798

grid = [[0] * 300 for _ in range(300)]
for x, y in ((x, y) for x in range(300) for y in range(300)):
    grid[x][y] = (((x + 10) * y + INPUT) * (x + 10)) % 1000 // 100 - 5

cache = {1: grid}
def find_max_power_subgrid(size):
    if size < 2:
        raise Exception("only use this function for cells 2x2 or bigger")
    if size - 1 not in cache:
        raise Exception("calculation for size - 1 needs to be called before")
    
    # initialize cache for this size
    cache[size] = [[0] * (301 - size) for _ in range(301 - size)]

    # calculate powers
    max_power = None
    for x, y in ((x,y) for x in range(301 - size) for y in range(301 - size)):
        # get cached value for the square at X,Y sized size-1
        power = cache[size - 1][x][y]

        # sum the additional row and column
        power += sum(grid[x + dx][y + size - 1] for dx in range(size))
        power += sum(grid[x + size - 1][y + dy] for dy in range(size - 1))

        # cache for later
        cache[size][x][y] = power

        # save if it's the max power up to now
        if max_power is None or power > max_power:
            max_power = power
            coords = (x, y)
    
    return (max_power, f"{coords[0]},{coords[1]},{size}")

results = [(grid[x][y], f"{x},{y},1") for x in range(300) for y in range(300)]
results.sort()
results = [results[-1]]
results.extend(find_max_power_subgrid(size) for size in range(2, 301))
results.sort()

result = find_max_power_subgrid(3)
print(f"Part 1: max power coords={result[1]}")
print(f"Part 2: max power coords={results[-1][1]}")