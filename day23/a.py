from collections import defaultdict

with open('day23/input.txt', 'r') as input:
    connect2 = set([tuple(sorted(l.strip().split('-'))) for l in input.readlines()])
    c_conns = defaultdict(set)
    connect3 = set()
    for c2 in connect2:
        c_conns[c2[0]].add(c2[1])
        c_conns[c2[1]].add(c2[0])
    for c2 in connect2:
        conn0, conn1 = c_conns[c2[0]], c_conns[c2[1]]
        c3 = conn0.intersection(conn1)
        for third_guy in c3:
            connect3.add(tuple(sorted([c2[0], c2[1], third_guy])))
    starts_with_t = [c3 for c3 in connect3 if c3[0].startswith('t') or c3[1].startswith('t') or c3[2].startswith('t')]
    print(f'PART1: connect-3 with a "t" {len(starts_with_t)}')

    connectX = set()
    for c1, conns in c_conns.items():
        for c2 in conns:
            # for each fully-connected-graph which includes c1 and c2
            # if all remaining members are connected to both, create a new and larger fully-connect-graph
            new_fcgs = set()
            for fcg in connectX:
                others = fcg - {c1, c2}
                if len(others) == 0:
                    continue
                if others <= c_conns[c1] and others <= c_conns[c2]:
                    new_fcgs.add(frozenset(others | {c1, c2}))
            connectX.add(frozenset({ c1, c2 }))
            connectX.update(new_fcgs)
    largest_fcg = max([(len(c), c) for c in connectX], key=lambda cc: cc[0])
    password = ','.join(sorted(list(largest_fcg[1])))
    print(f'PART2: password = {password}')


        