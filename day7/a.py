
def concat_sub_result(result, acc):
    if str(result).startswith(str(acc)):
        return int(str(result)[len(str(acc)):])
    return None

def has_valid_combination(result, l, acc, check_concat):
    if len(l) == 0:
        return result if result == acc else 0
    if result < acc:
        return 0
    
    return max(
        has_valid_combination(result, l[1:], acc + int(l[0]), check_concat), 
        has_valid_combination(result, l[1:], acc * int(l[0]), check_concat),
        has_valid_combination(result, l[1:], int(str(acc) + l[0]), check_concat) if check_concat else 0)

with open('day7/input.txt', 'r') as input:
    equations = [(int(eq[0]), eq[1].strip().split(' ')) for eq in [l.strip().split(':') for l in input.readlines()]]
    calibrations2 = [has_valid_combination(result, components[1:], int(components[0]), False) for result, components in equations]
    calibrations3 = [has_valid_combination(result, components[1:], int(components[0]), True) for result, components in equations]

    print(f'PART1: sum of valid calibrations with 2 operators {sum(calibrations2)}')
    print(f'PART2: sum of valid calibrations with 3 operators {sum(calibrations3)}')


