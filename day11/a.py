from functools import cache

ITERATIONS_PART1 = 25
ITERATIONS_PART2 = 75

def evolve(stone):
    if stone == 0:
        return [1]
    stone_s = str(stone)
    if len(stone_s) % 2 == 0:
        return [int(stone_s[:len(stone_s)//2]), int(stone_s[len(stone_s)//2:])]
    return [stone * 2024]

@cache
def deep_count(stone, depth):
    return 1 if depth == 0 else sum([deep_count(s, depth-1) for s in evolve(stone)])

with open('day11/input.txt', 'r') as input:
    stones = [int(s) for s in input.read().strip().split()]

    print(f"PART1: number of stones {sum([deep_count(s, ITERATIONS_PART1) for s in stones])}")
    print(f"PART2: number of stones {sum([deep_count(s, ITERATIONS_PART2) for s in stones])}")
