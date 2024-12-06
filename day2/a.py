from functools import reduce 

num_safe_reports = 0
def is_safe(report):
    variance = []
    for i in range(len(report) - 1):
        variance.append(report[i+1] - report[i])
    distances_valid = all(1 <= abs(v) <= 3 for v in variance)
    all_positives = all(v>0 for v in variance)
    all_negatives = all(v<0 for v in variance)
    return distances_valid and (all_positives or all_negatives)

with open('day2/input.txt', 'r') as input:
    for l in input.readlines():
        report = [int(level) for level in l.strip().split(' ')]
        if is_safe(report):
            num_safe_reports += 1

print(f'PART1: number of safe reports = {num_safe_reports}')      

# this could be made faster with an iterative checker which permits one skip
num_safe_reports = 0
with open('day2/input.txt', 'r') as input:
    for l in input.readlines():
        report = [int(level) for level in l.strip().split(' ')]
        if is_safe(report):
            num_safe_reports += 1
        else:
            for removal in range(0, len(report)):
                if is_safe(report[:removal] + report[removal+1:]):
                    num_safe_reports += 1
                    break

print(f'PART2: number of safe reports = {num_safe_reports}')   