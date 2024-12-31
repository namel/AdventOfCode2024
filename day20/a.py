from lib.utils import *

LONG_JUMP = 20
JUMP_RADIUS = [(dy, dx) for dx in range(-LONG_JUMP, LONG_JUMP+1) for dy in range(-LONG_JUMP, LONG_JUMP+1) if abs(dx) + abs(dy) <= LONG_JUMP]

def get_jump_elements(pos, map):
    jumps = []
    for dy, dx in NEXT_POS_STRAIGHT:
        j1, j2 = (pos[0] + dy, pos[1] + dx), (pos[0] + 2*dy, pos[1] + 2*dx)
        if in_bounds(j2, map) and get_map_el(j1, map) == '#' and get_map_el(j2, map) in '.E':
            jumps.append((j1, j2))
    return jumps

def get_radius_elements(pos, map):
    jumps = []
    for dy, dx in JUMP_RADIUS:
        j = (pos[0] + dy, pos[1] + dx)
        if in_bounds(j, map) and get_map_el(j, map) in '.E':
            jumps.append((j, abs(dx) + abs(dy)))
    return jumps

with open('day20/input.txt', 'r') as input:
    map = [l.strip() for l in input.readlines()]
    start, end = find_element_in_map('S', map), find_element_in_map('E', map)

    pos, dist, path_distances, path_sequence, jumps, long_jumps = start, 0, {}, [start], 0, 0
    while pos != end:
        for next_pos, el in get_map_adjacent_elements(pos, map):
            if el in '.E' and next_pos not in path_distances:
                pos, dist = next_pos, dist + 1
                path_distances[pos] = dist
                path_sequence.append(pos)

    for dist, pos in enumerate(path_sequence):
        for el1, el2 in get_jump_elements(pos, map):
            jumps += 1 if path_distances[el2] > dist + 100 else 0

    for dist, pos in enumerate(path_sequence):
        radius_el = get_radius_elements(pos, map)
        for jump, jump_dist in radius_el:
            long_jumps += 1 if path_distances[jump] - dist - jump_dist >= 100 else 0
                

    print(f'PART1: 2-jumps that save 100 picoseconds {jumps}')
    print(f'PART2: 20-jumps that save 100 picoseconds {long_jumps}')
