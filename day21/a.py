from collections import namedtuple
from functools import cache

BOTTOM_LEFT, TOP_LEFT = (3,0), (0,0)
NUMBER_PAD = { 'A': (3,2), '0': (3,1), '1': (2,0), '2': (2,1), '3': (2,2), '4': (1,0), '5': (1,1), '6': (1,2), '7': (0,0), '8': (0,1), '9': (0,2) }
ARROW_PAD = { 'A': (0, 2), '<':(1,0), '>':(1,2), '^':(0,1), 'v':(1,1) }
ARROW_MOVE = { '<':(0,-1), '>':(0,1), '^':(-1,0), 'v':(1,0) }

Robot = namedtuple('Robot', ['pos', 'pad', 'gap'])
robots = [[Robot((3,2), NUMBER_PAD, BOTTOM_LEFT)] + [Robot((0,2), ARROW_PAD, TOP_LEFT) for i in range(2)],
    [Robot((3,2), NUMBER_PAD, BOTTOM_LEFT)] + [Robot((0,2), ARROW_PAD, TOP_LEFT) for i in range(25)]]

dy_pattern = lambda dy: '^' * abs(dy) if dy < 0 else 'v' * dy
dx_pattern = lambda dx: '<' * abs(dx) if dx < 0 else '>' * dx

def generate_paths(dy, dx):
    if (dy,dx) == (0,0):
        return ['']
    paths = []
    for ddy in range(min(0, dy), max(0, dy)+1):
        for ddx in range(min(0, dx), max(0, dx)+1):
            if (ddy, ddx) != (0,0):
                paths.extend([dy_pattern(ddy) + dx_pattern(ddx) + pp for pp in generate_paths(dy-ddy, dx-ddx)])
    return list(set(paths))

def hits_gap(pos, path, gap):
    for p in path:
        pos = (pos[0] + ARROW_MOVE[p][0], pos[1] + ARROW_MOVE[p][1])
        if pos == gap:
            return True
    return False

@cache
def shortest_sequence(button_sequence, robot_id, robot_set):
    sequences = []
    for b in button_sequence:
        rob = robots[robot_set][robot_id]
        dy, dx = rob.pad[b][0] - rob.pos[0], rob.pad[b][1] - rob.pos[1]
        all_paths = [p+'A' for p in generate_paths(dy, dx) if not hits_gap(rob.pos, p, rob.gap)]
        if robot_id < len(robots[robot_set]) - 1:
            shortest = min([shortest_sequence(p, robot_id + 1, robot_set) for p in all_paths])
        else:
            shortest = len(all_paths[0])
        sequences.append(shortest)
        robots[robot_set][robot_id] = Robot(rob.pad[b], rob.pad, rob.gap)
    return sum(sequences)

with open('day21/input.txt', 'r') as input: 
    codes = [l.strip() for l in input.readlines()]   
    part1 = [(code, int(code[:-1]) * shortest_sequence(code, 0, 0)) for code in codes]
    part2 = [(code, int(code[:-1]) * shortest_sequence(code, 0, 1)) for code in codes]
    print(f'PART1: codes: {part1}\ncomplexity {sum([p[1] for p in part1])}\n')
    print(f'PART2: codes: {part2}\ncomplexity {sum([p[1] for p in part2])}\n')
