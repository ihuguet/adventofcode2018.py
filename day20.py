#!/usr/bin/env python3

with open("day20_in.txt") as f:
    regex = f.read().strip()[1:-1]

class Room:
    def __init__(self, min_steps):
        self.doors = set()
        self.min_steps = min_steps
        self.regex_indexes = set()

class Path:
    def __init__(self, pos, steps, regex_str_chunks):
        self.pos = pos
        self.steps = steps
        self.regex_str_chunks = regex_str_chunks

moves = {
    'N': ('S', (1, 0)),
    'S': ('N', (-1, 0)),
    'E': ('W', (0, 1)),
    'W': ('E', (0, -1))
}

def follow_regex_path(regex_str):
    pos, steps = (0, 0), 0
    rooms = {pos: Room(steps)}
    path = Path(pos, steps, [(0, len(regex_str))])
    paths = []

    while path or paths:
        if not path:
            path = paths.pop()
            pos, steps = path.pos, path.steps
        
        if not path.regex_str_chunks:
            path = None
            continue

        chunk = path.regex_str_chunks.pop()
        idx, end = chunk

        while idx < end:
            ch = regex_str[idx]

            if ch == "(":
                branches, idx = parse_branches(regex_str, idx)
                chunks = path.regex_str_chunks
                chunks.append((idx, end))  # add resting part of current chunk

                for branch in branches:
                    branch_chunks = chunks.copy() + [branch]
                    paths.append(Path(pos, steps, branch_chunks))
                
                path = None
                break

            elif ch in "NESW":
                rooms[pos].doors.add(ch)
                door_next, pos_move = moves[ch]

                pos = (pos[0] + pos_move[0], pos[1] + pos_move[1])
                steps += 1

                # early exit from this branch if it has been visited with same position in the regex
                if pos in rooms and idx in rooms[pos].regex_indexes:
                    break

                room = rooms.setdefault(pos, Room(steps))
                room.regex_indexes.add(idx)
                room.doors.add(door_next)
                if steps < room.min_steps:
                    room.min_steps = steps

            idx += 1
        
    return rooms

def parse_branches(path, idx):
    nest_lvl = 0
    idx += 1
    idx_start = idx
    branches = []

    while idx < len(path):
        ch = path[idx]

        if ch == "(":
            nest_lvl += 1
        elif ch == ")" and nest_lvl > 0:
            nest_lvl -= 1
        elif ch == "|" and nest_lvl == 0:
            branches.append((idx_start, idx))
            idx_start = idx + 1
        elif ch == ")":
            branches.append((idx_start, idx))
            return branches, idx + 1
        
        idx += 1

def get_furthest_room(rooms):
    return max(map(lambda r: r.min_steps, rooms.values()))

def count_rooms_with_dist_gte(rooms, dist):
    return sum(1 for _ in filter(lambda r: r.min_steps >= dist, rooms.values()))

def print_rooms(rooms):
    x_min = min(map(lambda p: p[1], rooms))
    x_max = max(map(lambda p: p[1], rooms))
    y_min = min(map(lambda p: p[0], rooms))
    y_max = max(map(lambda p: p[0], rooms))

    for y in range(y_max, y_min - 1, -1):
        for x in range(x_min, x_max + 1):
            if (room := rooms.get((y, x))) is not None:
                print('#', '-' if 'N' in room.doors else '#', sep='', end='')
            elif room_n_nw_w(y, x):
                print('#', '#' if rooms.get((y + 1, x)) is not None else ' ', sep='', end='')
            else:
                print('  ', end='')
        print('#' if room_n_nw_w(y, x_max + 1) else '')
        for x in range(x_min, x_max + 1):
            if (room := rooms.get((y, x))) is not None:
                room_ch = 'X' if (y, x) == (0, 0) else '.'
                print('|' if 'W' in room.doors else '#', room_ch, sep='', end='')
            elif rooms.get((y, x - 1)) is not None:
                print('# ', end='')
            else:
                print('  ', end="")
        print('#' if room is not None else '')
    for x in range(x_min, x_max + 1):
        if (room := rooms.get((y_min, x))) is not None:
            print('#', '-' if 'S' in room.doors else '#', sep='', end='')
        elif rooms.get((y_min, x - 1)) is not None:
            print('# ', end='')
        else:
            print('  ', end='')
    print('#' if room is not None else '')

def room_n_nw_w(y, x):
    return (rooms.get((y + 1, x)) is not None
        or rooms.get((y + 1, x -1)) is not None
        or rooms.get((y, x - 1)) is not None)

# tests
# regex = "ENWWW(NEEE|SSE(EE|N))"
# regex  = "ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN"
# regex = "ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))"
# regex = "WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))"

rooms = follow_regex_path(regex)
# print_rooms(rooms)

print(f"Part 1: furthest room is {get_furthest_room(rooms)} doors away")
print(f"Part 2: {count_rooms_with_dist_gte(rooms, 1000)} rooms 1000+ doors away")