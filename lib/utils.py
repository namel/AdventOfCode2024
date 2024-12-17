NEXT_POS_ALL = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  
NEXT_POS_STRAIGHT = [(-1, 0), (0, -1), (0, 1), (1, 0)]


in_bounds = lambda pos, map: (0 <= pos[0] < len(map)) and (0 <= pos[1] < len(map[0]))
get_map_el = lambda pos, map: map[pos[0]][pos[1]]
get_map_adjacent = lambda pos, map: [p for p in [(pos[0] + dy, pos[1] + dx) for dy, dx in NEXT_POS_STRAIGHT] if in_bounds(p, map)]
get_map_adjacent_elements = lambda pos, map: [(p, map[p[0]][p[1]]) for p in get_map_adjacent(pos, map)]
