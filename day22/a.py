from collections import defaultdict

def calc_secret(s):
    s = ((s * 64) ^ s) % 16777216
    s = ((s // 32) ^ s) % 16777216
    s = ((s * 2048) ^ s) % 16777216
    return s

def depth_calc(s, n):
    for i in range(n):
        s.append(calc_secret(s[-1]))
    return s

get_seq = lambda s, ix: tuple([s[d+1]-s[d] for d in range(ix, ix+4)])
def collect_sequences(monkey, sequences):
    visited_seq = set()
    singles = [step % 10 for step in monkey]
    for i in range(0, len(singles)-4):
        seq = get_seq(singles, i)
        if seq in visited_seq:
            continue
        sequences[seq].append(singles[i+4])
        visited_seq.add(seq)

with open('day22/input.txt', 'r') as input:
    secrets = [int(l.strip()) for l in input.readlines()]
    monkey_seqs = [depth_calc([s], 2000) for s in secrets]
    print(f'PART1: sum of cycles {sum([monkey[-1] for monkey in monkey_seqs])}')

    sequences = defaultdict(list)
    [collect_sequences(monkey, sequences) for monkey in monkey_seqs]
    sequence_bananas = defaultdict(int)
    for s in sequences:
        sequence_bananas[s] = sum(sequences[s])
    best_price = max(sequence_bananas.values())
    best_sequence = [s for s in sequence_bananas if sequence_bananas[s] == best_price]
    print(f'PART2: {best_price} at sequence {best_sequence}')
