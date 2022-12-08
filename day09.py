#!/usr/bin/env python3

PLAYERS = 452
MARBLES = 71250

class Node:
    def __init__(self, value):
        self.value = value
        self.next = self
        self.prev = self

class Circle:
    def __init__(self):
        self.marbles = Node(0)
        self.current = self.marbles
    
    def move_cw(self, count):
        while count > 0:
            self.current = self.current.next
            count -= 1
    
    def move_ccw(self, count):
        while count > 0:
            self.current = self.current.prev
            count -= 1
    
    def insert(self, value):
        node = Node(value)
        prev, next = self.current.prev, self.current
        prev.next = node
        next.prev = node
        node.prev = prev
        node.next = next
        self.current = node

    def pop(self):
        node = self.current
        prev, next = node.prev, node.next
        prev.next = next
        next.prev = prev
        self.current = next
        return node.value

def play(marbles_count):
    circle = Circle()
    players = [0] * PLAYERS
    player = 0

    for next_value in range(1, marbles_count + 1):
        if next_value % 23 != 0:
            circle.move_cw(2)
            circle.insert(next_value)
        else:
            players[player] += next_value
            circle.move_ccw(7)
            players[player] += circle.pop()
        
        player = player + 1 if player < PLAYERS - 1 else 0
    
    return max(players)

print(f"Part 1: max score={play(MARBLES)}")
print(f"Part 2: max score={play(MARBLES * 100)}")
        