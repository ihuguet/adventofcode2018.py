#/usr/bin/env python3

with open("day18_in.txt") as f:
    lines = [l.strip() for l in f]
    grid = ''.join(lines)

Y_END = len(lines)
X_END = len(lines[0])

def run(grid, times):
    cache = {grid: 0}

    i = 0
    while i < times:
        grid = next_grid(grid)

        if grid in cache:
            i = iterations_fast_jump(i, cache[grid], times)
            cache.clear()
        
        cache[grid] = i
        i += 1

    return grid.count('|') * grid.count('#')

def next_grid(grid):
    return ''.join(next_grid_generator(grid))

def next_grid_generator(grid):
    for y, x in ((y, x) for y in range(Y_END) for x in range(X_END)):
        val = grid[y * X_END + x]
        adjs = list(adjacents(grid, y, x))

        if val == '.' and adjs.count('|') >= 3:
            val = '|'
        elif val == '|' and adjs.count('#') >= 3:
            val = '#'
        elif val == '#' and (adjs.count('#') == 0 or adjs.count('|') == 0):
            val = '.'

        yield val

def adjacents(grid, y, x):
    ymin, xmin = max(y - 1, 0), max(x - 1, 0)
    yend, xend = min(y + 2, Y_END), min(x + 2, X_END)
    for y2, x2 in ((y2, x2) for y2 in range(ymin, yend) for x2 in range(xmin, xend)):
        if (y2 != y or x2 != x):
            yield grid[y2 * X_END + x2]

def iterations_fast_jump(i, i_prev, i_max):
    jump = i - i_prev
    jumps = (i_max - 1 - i) // jump
    return i + jump * jumps

print(f"Part 1: trees * lumberyards = {run(grid, 10)}")
print(f"Part 2: trees * lumberyards = {run(grid, 1000000000)}")