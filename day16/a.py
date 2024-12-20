from lib.utils import *

lowest_score, lowest_score_positions, map, visited = 1000000, set(), [], {}
advance = lambda pos, direction: (pos[0] + NEXT_POS_STRAIGHT[direction][0], pos[1] + NEXT_POS_STRAIGHT[direction][1])

def get_item_in_direction(pos, direction):
    next_pos = advance(pos, direction)
    return map[next_pos[0]][next_pos[1]]

def get_next_pos(pos, direction):
    nexts = []
    for i in [ -1, 0, 1]:
        new_direction = (direction + i ) % 4
        if get_item_in_direction(pos, new_direction) in '.E':
            nexts.append((advance(pos, new_direction), new_direction))
    return nexts

def traverse_map(pos, direction, end, score, path):
    global lowest_score, lowest_score_positions
    path.add(pos)
    nexts = get_next_pos(pos, direction)
    while len(nexts) == 1:
        score += 1 if nexts[0][1] == direction else 1001
        pos, direction = nexts[0]
        path.add(pos)
        if pos == end:
            if score == lowest_score:
                lowest_score_positions.update(path)
            elif score < lowest_score:
                lowest_score = score
                lowest_score_positions = path
            return
        nexts = get_next_pos(pos, direction)
    if len(nexts) == 0 or visited.get((pos, direction), 1000000) < score:
        return
    visited[(pos, direction)] = score
    for next_pos, next_direction in nexts:
        traverse_map(next_pos, next_direction, end, score + 1 if direction == next_direction else score + 1001, path.copy())

with open('day16/input.txt', 'r') as input:
    map = [l.strip() for l in input.readlines()]
    traverse_map(find_element_in_map('S', map), 1, find_element_in_map('E', map), 0, set())
    print(f'PART1: lowest_score is {lowest_score}')
    print(f'PART1: positions in lowest-score paths is {len(lowest_score_positions)}')
