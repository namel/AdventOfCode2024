NEXT_POS_INCR = [(0, -1), (1, 0), (0, 1), (-1, 0)]  

get_next_pos = lambda pos, direction: (pos[0] + NEXT_POS_INCR[direction][0], pos[1] + NEXT_POS_INCR[direction][1])
get_map_element = lambda pos, map_lines: map_lines[pos[1]][pos[0]] if 0 <= pos[0] < len(map_lines[0]) and 0 <= pos[1] < len(map_lines) else None
looping_obstructions_count = 0

# I think you actually have to place an obstacle there, because it can bounce twice
def travel(pos, direction, visited, map_lines, generate_obstacle):
    global looping_obstructions_count
    while get_map_element(pos, map_lines) is not None:
        if not generate_obstacle and (pos, direction) in visited:
            looping_obstructions_count += 1
            return
        visited.add((pos, direction))
        next_pos = get_next_pos(pos, direction)
        while get_map_element(next_pos, map_lines) == '#':
            direction = (direction + 1) % 4
            next_pos = get_next_pos(pos, direction)
        if generate_obstacle and get_map_element(next_pos, map_lines) in ['.', '^'] and next_pos not in set([v[0] for v in visited]):
            map_lines[next_pos[1]][next_pos[0]] = '#'
            travel(pos, (direction + 1) % 4, visited.copy(), map_lines, False)
            map_lines[next_pos[1]][next_pos[0]] = '.'
        pos = next_pos
        
# re-write this with a traversal than can call itself.
# keep only the one visited (but make it directional)
with open('day6/input.txt', 'r') as input:
    map_lines = [[c for c in line] for line in input.readlines()]
    guard_pos = [(guard_row.index('^'), guard_row_ix) for guard_row_ix, guard_row in enumerate(map_lines) if '^' in guard_row][0]
    visited = set()
    travel(guard_pos, 0, visited, map_lines, True)

    print(f"PART1: number of visited guard positions {len(set([v[0] for v in visited]))}")
    print(f"PART2: number of looping obstructions {looping_obstructions_count}")

        