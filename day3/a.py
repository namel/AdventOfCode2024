import re

ignore_multiply_actions = False

def get_multiply_action(section, check_do):
    global ignore_multiply_actions
    if check_do:
        if ignore_multiply_actions:
            if 'do()' == section[0:4]:
                ignore_multiply_actions = False
            return 0
        if 'don\'t()' == section[0:7]:
            ignore_multiply_actions = True
            return 0
    if len(section) < 8:
        return 0
    if 'mul(' != section[0:4]:
        return 0
    m = re.match(r'mul\(([1-9][0-9]?[0-9]?),([1-9][0-9]?[0-9]?)\).*', section)
    if m is None:
        return 0    
    return int(m.group(1)) * int(m.group(2))

def scan_input(check_do):
    all_multiplies = 0
    with open('day3/input.txt', 'r') as input:
        program = input.read()
        for start in range(0, len(program)):
            end = min(start + 12, len(program))
            all_multiplies += get_multiply_action(program[start:end], check_do)
    return all_multiplies

print(f"PART1: all multiplies add to: {scan_input(False)}")
print(f"PART2: all multiplies add to: {scan_input(True)}")
