from collections import defaultdict
from lib.utils import get_map_adjacent_elements, get_map_el

PERIMETER_FIX = { 4:-4, 3:-2, 2:0, 1:2, 0:4 }

def get_adjacent_pos(pos, map):
    id = get_map_el(pos, map)
    adjacents = get_map_adjacent_elements(pos, map)
    return set([a[0] for a in adjacents if a[1] == id]), set([a[0] for a in adjacents if a[1] != id])

def explore(need_checking, map):
    area = need_checking.copy()
    outside = set()
    while len(need_checking) > 0:
        new_connected_pos = need_checking.pop()
        area.add(new_connected_pos)
        connected, disconnected = get_adjacent_pos(new_connected_pos, map)
        need_checking.update(connected - area)
        outside.update(disconnected)
    all_ranges.append(area)
    assigned.update(area)
    return outside

def perimeter_update(scanned, pos):
    adjacents = set([(pos[0] + dy, pos[1] + dx) for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)]])
    return PERIMETER_FIX[len(adjacents.intersection(scanned))]
        
def price(area):
    scanned, perimiter = set(), 0
    for pos in area:
        perimiter += perimeter_update(scanned, pos)
        scanned.add(pos)
    return perimiter * len(scanned)

def discover_sides(points1, points2):
    start, stop = min(points1 + points2), max(points1 + points2)
    sides, current = 0, 0
    for p in range(start, stop + 1):
        if (p in points1) ^ (p in points2):
            if (current == 0 or current == 2) or (p in points1) ^ (p-1 in points1):
                sides += 1
        current = int(p in points1) + int(p in points2)
    return sides

def scan_layer(area, horizontal):
    sides, layers, prev_layer = 0, defaultdict(list), []
    for p in area:
        layers[p[0 if horizontal else 1]].append(p)
    for l in [layers[l] for l in sorted([k for k in layers.keys()])] + [[]]:
        layer = [p[1 if horizontal else 0] for p in l]
        sides += discover_sides(prev_layer, layer)
        prev_layer = layer
    return sides

def price2(area):
    return len(area) * (scan_layer(area, horizontal=True) + scan_layer(area, horizontal=False))
    
all_ranges, assigned = [], set()
with open('day12/input.txt', 'r') as input:
    map = [l.strip() for l in input.readlines()]
    unexplored = {(0,0)}
    while len(unexplored) > 0:
        unexplored |= explore({unexplored.pop()}, map)
        unexplored.difference_update(assigned)
    print(f'PART1: sum of perimiter-prices {sum([price(area) for area in all_ranges])}')
    print(f'PART2: sum of sides-prices {sum([price2(area) for area in all_ranges])}')
