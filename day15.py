#!/usr/bin/env python3

import heapq
import copy

class Unit:
    def __init__(self, team, damage=3):
        self.team = team
        self.life = 200
        self.damage = damage

class Combat:
    def __init__(self, cave_str, elfs_damage=3):
        self.cave = [list(l.strip()) for l in cave_str.splitlines()]

        self.units = {}
        for y, row in enumerate(self.cave):
            for x, square in enumerate(row):
                if square == 'G':
                    self.units[(y, x)] = Unit('G')
                    self.cave[y][x] = "."
                elif square == 'E':
                    self.units[(y, x)] = Unit('E', elfs_damage)
                    self.cave[y][x] = "."

    def _adjacents(pos):
        y, x = pos
        return [(y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)]

    def adjacents_free(self, pos):
        for y, x in Combat._adjacents(pos):
            if self.cave[y][x] == '.' and (y, x) not in self.units:
                yield y, x

    def count_alive_team_units(self, team):
        return len([u for u in self.units.values() if u.team == team])

    def count_alive_enemy_units(self, team):
        return len([u for u in self.units.values() if u.team != team])

    def get_enemy_in_range(self, pos, team):
        enemies = []
        min_life = 200

        for adj_pos in Combat._adjacents(pos):
            enemy = self.units.get(adj_pos)
            if (enemy is not None and team != enemy.team):
                if enemy.life < min_life:
                    enemies = [adj_pos]
                    min_life = enemy.life
                elif enemy.life == min_life:
                    heapq.heappush(enemies, adj_pos)
        
        return enemies[0] if enemies else None

    def get_step_towards_enemy(self, orig_pos):
        distances = copy.deepcopy(self.cave)
        queue = [(0, orig_pos)]
        destinations = []
        min_dist = None
        team = self.units[orig_pos].team

        # find closest position adjacent to an enemy (more than one in case of tie)
        while queue:
            dist, pos = heapq.heappop(queue)

            if destinations and dist > min_dist:
                break

            if self.get_enemy_in_range(pos, team) is not None:
                heapq.heappush(destinations, pos)  # dist == min_dist
                min_dist = dist
                continue

            for y, x in self.adjacents_free(pos):
                if distances[y][x] == '.':
                    distances[y][x] = dist + 1
                    heapq.heappush(queue, (dist + 1, (y, x)))

        # no ememies reachable?
        if not destinations:
            return None

        # if found more than one, choose in reading order (first of sorted list)
        # do the path(s) backwards to get possible next step position
        queue = [(min_dist, destinations[0])]
        destinations = []
        while queue:
            dist, pos = heapq.heappop(queue)

            if dist == 1:
                heapq.heappush(destinations, pos)
                continue

            for y, x in self.adjacents_free(pos):
                if distances[y][x] == dist - 1:
                    distances[y][x] = 'x'
                    heapq.heappush(queue, (dist - 1, (y, x)))
            
        # if found more than one, choose in reading order (first of sorted list)
        return destinations[0]

    def attack(self, enemy_pos, damage):
        self.units[enemy_pos].life -= damage
        if self.units[enemy_pos].life <= 0:
            del self.units[enemy_pos]  # dead!

    def combat(self, elfs_damage=3):
        rounds = 0
        while True:
            pending = [pos for pos in self.units]
            pending.sort(reverse=True)

            while pending:
                pos = pending.pop()

                if pos not in self.units:  # killed this round
                    continue

                unit = self.units[pos]

                if self.count_alive_enemy_units(unit.team) == 0:
                    return rounds * sum(unit.life for unit in self.units.values())

                enemy_pos = self.get_enemy_in_range(pos, unit.team)

                if enemy_pos is None:
                    new_pos = self.get_step_towards_enemy(pos)
                    if new_pos is not None:
                        del self.units[pos]
                        self.units[new_pos] = unit
                        enemy_pos = self.get_enemy_in_range(new_pos, unit.team)

                if enemy_pos is not None:
                    self.attack(enemy_pos, unit.damage)
            
            rounds += 1

with open("day15_in.txt") as f:
    cave_str = f.read()

combat = Combat(cave_str)
print(f"Part 1: combat result = {combat.combat()}")

elfs_damage = 4
while True:
    combat = Combat(cave_str, elfs_damage)
    elfs_num = combat.count_alive_team_units('E')
    result = combat.combat()
    if combat.count_alive_team_units('E') == elfs_num:
        break
    elfs_damage += 1

print(f"Part 2: min required elfs damage = {elfs_damage}, combat result = {result}")
