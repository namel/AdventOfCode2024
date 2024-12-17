from collections import namedtuple

Machine = namedtuple('Machine', ['buttonA', 'buttonB', 'prize'])

# Given two equations of two variables a and b:
#     C0 = BA0*a + BB0*b
#     C1 = BA1*a + BB1*b
#
# we solve for b:
#    a = (C0 - BB0*b)/BA0
#    a = (C1 - BB1*b)/BA1
#
#    -> (C0 - BB0*b)*BA1 = (C1 - BB1*b)*BA0
#    -> C0*BA1 - C1*BA0 = b* ((BB0*BA1) - (BB1*BA0))
#    -> b = [C0*BA1 - C1*BA0] / ((BB0*BA1) - (BB1*BA0))
#
def solve_machine(m):
    B = (m.prize[0] * m.buttonA[1] - m.prize[1] * m.buttonA[0]) / (m.buttonB[0] * m.buttonA[1] - m.buttonB[1] * m.buttonA[0]) 
    A1 = (m.prize[0] - m.buttonB[0] * B) / m.buttonA[0]
    A2 = (m.prize[1] - m.buttonB[1] * B) / m.buttonA[1]
    if A1 == A2 and A1.is_integer() and B.is_integer():
        return A1, B
    return 0, 0

big_machine = lambda m: Machine(m.buttonA, m.buttonB, [m.prize[0] + 10000000000000, m.prize[1] + 10000000000000])
get_xy = lambda l: [int(c.strip(' XY+=')) for c in l.strip().split(':')[1].split(',')]

with open('day13/input.txt', 'r') as input:
    lines = input.readlines()
    tokens1, tokens2 = 0, 0
    for i in range(0, len(lines), 4):
        m = Machine(get_xy(lines[i]), get_xy(lines[i+1]), get_xy(lines[i+2]))
        aPress, bPress = solve_machine(m)
        tokens1 += 3 * aPress + bPress
        aPress, bPress = solve_machine(big_machine(m))
        tokens2 += 3 * aPress + bPress
    print(f'PART1: number of tokens {tokens1}')
    print(f'PART2: number of tokens {tokens2}')
