#!/usr/bin/env python3

with open("day08_in.txt", "r") as f:
    data = [int(n) for n in f.readline().strip().split(" ")]

class Node:
    def __init__(self, children, metadata):
        self.children_count = children
        self.metadata_count = metadata
        self.children_vals = []
        self.metadata = None
        self.value = self.val_with_children if children > 0 else self.val_no_children
    
    def val_no_children(self):
        return sum(self.metadata)

    def val_with_children(self):
        accum = 0
        for child in self.metadata:
            if child > 0 and child <= len(self.children_vals):
                accum += self.children_vals[child - 1]
        return accum

#data = [int(n) for n in "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split(" ")]
part1_sum = 0
stack = []
node = Node(data[0], data[1])
idx = 2

while idx < len(data):
    if node.children_count == 0:
        node.metadata = data[idx:idx + node.metadata_count]
        idx += node.metadata_count

        part1_sum += sum(node.metadata)
        
        if stack:
            child_val = node.value()
            node = stack.pop()
            node.children_vals.append(child_val)
            node.children_count -= 1

    if node.children_count > 0:
        stack.append(node)
        node = Node(data[idx], data[idx + 1])
        idx += 2

print(f"Part 1: metadata sum={part1_sum}")
print(f"Part 2: root node value={node.value()}")