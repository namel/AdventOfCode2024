from collections import defaultdict

def build_designs(d, sub_designs, towels):
    arrangements = 0
    for t in towels:
        for sd in sub_designs:
            if d == t + sd:
                arrangements += sub_designs[sd]
    sub_designs[d] += arrangements
    return

with open('day19/input.txt', 'r') as input:
    l = input.readlines()
    towels = [t.strip() for t in l[0].strip().split(',')]
    designs = [d.strip() for d in l[2:]]
    num_possible, num_arrangements = 0, 0

    for d in designs:
        sub_designs = defaultdict(int)
        sub_designs[''] = 1
        for l in range(1, len(d)+1):
            build_designs(d[-l:], sub_designs, towels)
        num_possible += int(sub_designs[d] > 0)
        num_arrangements += sub_designs[d]

    print(f'PART1: number of possible design: {num_possible}')
    print(f'PART2: number of possible design arrangements: {num_arrangements}')
