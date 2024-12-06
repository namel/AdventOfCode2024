NEXT_POS_INCR = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  
XMAS = 'XMAS'

get_letter = lambda pos, lines: lines[pos[0]][pos[1]] if (0 <= pos[0] < len(lines)) and (0 <= pos[1] < len(lines[0])) else None

def confirm_word(pos, direction, lines, depth):
    if depth == len(XMAS)-1:
        return int(get_letter(pos, lines) == 'S')
    return int(get_letter(pos, lines) == XMAS[depth] and confirm_word(get_next_pos(pos, direction), direction, lines, depth + 1))

def get_next_pos(pos, direction = None):
    if direction is None:
        return [((pos[0] + dx, pos[1] + dy), ind) for ind, (dx, dy) in enumerate(NEXT_POS_INCR)]
    return (pos[0] + NEXT_POS_INCR[direction][0], pos[1] + NEXT_POS_INCR[direction][1])

def check_pos(row, col, lines):
    if (lines[row][col] == 'X'):
        return sum([confirm_word(next_pos, direction, lines, 1) for next_pos, direction in get_next_pos((row, col))])
    return 0

def check_cross(row, col, lines):
    if (lines[row][col] == 'A'):
        diag1 = { get_letter(get_next_pos((row, col), 0), lines), get_letter(get_next_pos((row, col), 7), lines) }
        diag2 = { get_letter(get_next_pos((row, col), 2), lines), get_letter(get_next_pos((row, col), 5), lines) }
        return int(diag1 == diag2 == { 'M', 'S' })
    return 0

with open('day4/input.txt', 'r') as input:
    lines = input.readlines()
    pos_XMAS = [check_pos(row, col, lines) for col in range(len(lines[0])) for row in range(len(lines))]
    pos_CROSS_MAS = [check_cross(row, col, lines) for col in range(len(lines[0])) for row in range(len(lines))]
    print(f'PART1: XMAS count is {sum(pos_XMAS)}')
    print(f'PART2: CROSS-MAS count is {sum(pos_CROSS_MAS)}')
    