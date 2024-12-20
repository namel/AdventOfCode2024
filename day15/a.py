DIRECTIONS = { '<': (0, -1), '^': (-1, 0), '>': (0, 1), 'v': (1, 0) }
WIDE_ELEMENT = { '#': '##', 'O': '[]', '.': '..', '@': '@.' }

get_pos = lambda dist, pos, direction: (pos[0] + direction[0] * dist, pos[1] + direction[1] * dist)
get_item = lambda dist, pos, direction, map: map[pos[0] + direction[0] * dist][pos[1] + direction[1] * dist]

def set_item(dist, pos, direction, map, item):
    map[pos[0] + direction[0] * dist][pos[1] + direction[1] * dist] = item

def offset_of(item, pos, direction, map):
    dist = 0
    while get_item(dist, pos, direction, map) != item:
        dist += 1
    return dist

def push(pos, direction, map):
    push_dist = 1
    while get_item(push_dist, pos, direction, map) == 'O':
        push_dist += 1
    if get_item(push_dist, pos, direction, map) != '.':
        return pos
    set_item(push_dist, pos, direction, map, 'O')
    set_item(1, pos, direction, map, '@')
    set_item(0, pos, direction, map, '.')
    return get_pos(1, pos, direction)
            
def move_level(points, level, direction, map):
    for p in points:
        map[level + direction[0]][p] = map[level][p]
        map[level][p] = '.'

def push_points(points, level, direction, map):
    next_points = [map[level + direction[0]][p] for p in points]
    if any([p == '#' for p in next_points]):
        return False
    if all([p == '.' for p in next_points]):
        move_level(points, level, direction, map)
        return True
    next_points = set()
    for p in points:
        if map[level + direction[0]][p] == '[':
            next_points.update({p, p+1})
        elif map[level + direction[0]][p] == ']':
            next_points.update({p, p-1})
    if push_points(next_points, level + direction[0], direction, map):
        move_level(points, level, direction, map)
        return True
    return False

def push_wide(pos, direction, map):

    # horizontal
    if direction[0] == 0:
        push_dist = 1
        while get_item(push_dist, pos, direction, map) in '[]':
            push_dist += 1
        if get_item(push_dist, pos, direction, map) != '.':
            return pos
        for i in range(push_dist, 0, -1):
            set_item(i, pos, direction, map, get_item(i-1, pos, direction, map))
        set_item(0, pos, direction, map, '.')
        return get_pos(1, pos, direction)
    
    # vertical
    if push_points({pos[1]}, pos[0], direction, map):
        return get_pos(1, pos, direction)
    return pos

with open('day15/input.txt', 'r') as input:
    map = [l.strip() for l in input.readlines()]
    instructions_start = [line_no for line_no, line in enumerate(map) if line == ''][0] + 1
    pos = [(line_no, line.find('@')) for line_no, line in enumerate(map[:instructions_start]) if '@' in line][0]
    pos_wide = (pos[0], pos[1] * 2)
    
    map2D = [[c for c in l] for l in map[:instructions_start-1]]
    for i in ''.join(map[instructions_start:]):
        pos = push(pos, DIRECTIONS[i], map2D)

    gps = [row*100 + col for row in range(len(map2D)) for col in range(len(map2D[0])) if map2D[row][col] == 'O']
    print(f'PART1: sum of GPS coordinate {sum(gps)}')

    wide_map = [''.join([WIDE_ELEMENT[c] for c in line]) for line in map[:instructions_start-1]]
    map2D = [[c for c in l] for l in wide_map[:instructions_start-1]]
    for i in ''.join(map[instructions_start:]):
        pos_wide = push_wide(pos_wide, DIRECTIONS[i], map2D)

    gps = [row*100 + col for row in range(len(map2D)) for col in range(len(map2D[0])) if map2D[row][col] == '[']
    print(f'PART2: sum of wide GPS coordinate {sum(gps)}')
