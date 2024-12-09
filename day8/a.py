from collections import defaultdict

vec_add = lambda p1, p2: (p1[0] + p2[0], p1[1] + p2[1])
get_next_pos = lambda p: (p[1][0] + p[1][0] - p[0][0], p[1][1] + p[1][1] - p[0][1])
is_inside_map = lambda p, lines: 0 <= p[0] < len(lines) and 0 <= p[1] < len(lines[0])

def generate_steps(pair, lines):
    delta = (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1])
    next_pos = pair[1]
    while is_inside_map(next_pos, lines):
        yield next_pos
        next_pos = vec_add(next_pos, delta)

with open('day8/input.txt', 'r') as input:
    lines = [[c for c in l.strip()] for l in input.readlines()]
    antennas = defaultdict(set)
    [antennas[c].add((row,col)) for row, l in enumerate(lines) for col, c in enumerate(l) if c != '.']
    multinodes, antinodes = set(), set()
    for a in antennas:
        a_pos_list = antennas[a]
        ordered_pairs = [(pos1, pos2) for pos1 in a_pos_list for pos2 in a_pos_list if pos1 != pos2]
        antinodes.update([get_next_pos(p) for p in ordered_pairs if is_inside_map(get_next_pos(p), lines)])
        [multinodes.add(x) for p in ordered_pairs for x in generate_steps(p, lines)]
    print(f"PART1: multinodes = {len(antinodes)}")
    print(f"PART2: repeat multinodes = {len(multinodes)}")
    