from collections import defaultdict

def get_paths(pos, step, map):
    paths = [(pos[0] + dy, pos[1] + dx) for dx, dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]]
    return [p for p in paths if 0 <= p[0] < len(map) and 0 <= p[1] < len(map[0]) and int(map[p[0]][p[1]]) == step]

with open('day10/input.txt', 'r') as input:
    map = [l.strip() for l in input.readlines()]
    
    # from highest altitude to lowest, set the exact set of reachable trail-ends for that position
    trails = {}
    trails[9] = {(row,col):{(row,col)} for row in range(len(map)) for col in range(len(map[0])) if map[row][col] == '9'}
    for step in range(8, -1, -1):
        trails[step] = defaultdict(set)
        for pos, ends in trails[step+1].items():
            for prev_pos in get_paths(pos, step, map):
                trails[step][prev_pos].update(ends)
    print(f"PART1: number of trailheads {sum([len(ends) for ends in trails[0].values()])}")
    
    # from highest altitude to lowest, set the exact set of distinct paths to trail-ends
    trails = {}
    trails[9] = {(row,col):{(row,col)} for row in range(len(map)) for col in range(len(map[0])) if map[row][col] == '9'}
    for step in range(8, -1, -1):
        trails[step] = defaultdict(set)
        for pos, paths_to_one_end in trails[step+1].items():
            for prev_pos in get_paths(pos, step, map):
                for path_to_end in paths_to_one_end:
                    trails[step][prev_pos].add((prev_pos, path_to_end))

    print(f"PART2: number of trails {sum([len(paths) for paths in trails[0].values()])}")

