from collections import deque
from lib.utils import get_map_adjacent_elements

MAP_WIDTH = 71
MAP_HEIGHT = 71
NUM_FALL = 1024

map = [['.' for n in range(MAP_WIDTH)] for m in range(MAP_HEIGHT)]
byte_map = {}
explore_fifo = deque()

def explore(dist):
    while len(explore_fifo) > 0:
        pos, dist = explore_fifo.pop()
        for next_pos, el in  get_map_adjacent_elements(pos, map):
            if el == '#' or (next_pos in byte_map and byte_map[next_pos] <= (dist+1)):
                continue
            byte_map[next_pos] = dist + 1
            explore_fifo.appendleft(((next_pos), dist + 1))

with open('day18/input.txt', 'r') as input:
    blocks = [(int(ll[0]), int(ll[1])) for ll in [l.strip().split(',') for l in input.readlines()]]
    for b in blocks[:NUM_FALL]:
        map[b[1]][b[0]] = '#'

    byte_map[(0,0)] = 0
    explore_fifo.appendleft(((0,0), 0))
    explore(0)
    print(f'PART1: the shortest path to end-position {byte_map[(MAP_HEIGHT-1, MAP_WIDTH-1)]}')

    next_byte_ix = NUM_FALL
    while True:
        map[blocks[next_byte_ix][1]][blocks[next_byte_ix][0]] = '#'
        byte_map = {}
        byte_map[(0,0)] = 0
        explore_fifo.appendleft(((0,0), 0))
        explore(0)
        if (MAP_HEIGHT-1, MAP_WIDTH-1) not in byte_map:
            break
        next_byte_ix += 1
    print(f'PART2: no path after adding byte at {blocks[next_byte_ix]}')

