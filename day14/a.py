from collections import defaultdict, namedtuple
from math import prod


NUM_ITER = 100
DIMENSIONS = 101,103
Robot = namedtuple('Robot', ['pos', 'vel'])

parse_pv = lambda l: [component.strip('pv=').split(',') for component in l.strip().split(' ')]
parse_robot = lambda pv: Robot((int(pv[0][0]), int(pv[0][1])), (int(pv[1][0]), int(pv[1][1])))
move_robot = lambda r: Robot(((r.pos[0] + r.vel[0]) % DIMENSIONS[0], (r.pos[1] + r.vel[1]) % DIMENSIONS[1]), r.vel)
def quadrant(r):
    if r.pos[0] < DIMENSIONS[0] // 2:
        if r.pos[1] < DIMENSIONS[1] // 2:
            return 0
        if r.pos[1] > DIMENSIONS[1] // 2:
            return 1
    if r.pos[0] > DIMENSIONS[0] // 2:
        if r.pos[1] < DIMENSIONS[1] // 2:
            return 2
        if r.pos[1] > DIMENSIONS[1] // 2:
            return 3    
    return 4

def show_map(pos_list):
    for y in range(DIMENSIONS[1]):
        line = ''
        for x in range(DIMENSIONS[0]):
            line += 'x' if (x,y) in pos_list else ' '
        print(line)

with open('day14/input.txt', 'r') as input:
    robots = [parse_robot(parse_pv(l)) for l in input.readlines()]
    for i in range(1, NUM_ITER*100):
        q_count = defaultdict(int)
        robots = [move_robot(r) for r in robots]
        for r in robots:
            q_count[quadrant(r)] += 1
        if i == NUM_ITER:
            print(f'PART1: product of quadrant counts {q_count[0] * q_count[1] * q_count[2] * q_count[3]}')
        
        # unusual graphs were found with low-numbered quadrants
        if min(q_count[0], q_count[1], q_count[2], q_count[3]) < 75:
            print('low-numbered quadrant')
            if i == 7687:
                print('PART2:')
                show_map([r.pos for r in robots])
            
    