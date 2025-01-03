with open('day25/input.txt', 'r') as input:
    lines = [l.strip() for l in input.readlines()]
    locks = [lines[offset:offset+7] for offset in range(0, len(lines), 8) if lines[offset] == '#####']
    keys = [lines[offset:offset+7] for offset in range(0, len(lines), 8) if lines[offset] == '.....']

    locks = [[ll.index('.') - 1 for ll in list(zip(*lock))] for lock in locks]
    keys = [[6 - kk.index('#') for kk in list(zip(*key))] for key in keys]
    fit_key_pairs = [(k,l) for k in keys for l in locks if all(map(lambda kl: sum(kl) <= 5, zip(k,l)))]

    print(f'PART1: number of key/lock working pairs is {len(fit_key_pairs)}')

