GATE_OP = { 'AND': (lambda x,y: x and y), 'OR': (lambda x,y: x or y), 'XOR': (lambda x,y: x ^ y) }

gate_swaps = {}
def circuit_tick(gates, wires):
    new_values = {}
    for g in gates:
        (arg1, op, arg2), output = g[0], g[1]
        if output in gate_swaps:
            output = gate_swaps[output]
        if arg1 in wires and arg2 in wires:
            new_values[output] = GATE_OP[op](wires[arg1], wires[arg2])
    wires.update(new_values)

def test_adder(wires, gates, bit, prevXY, curXY, expected_z):
    x,y,z = f"x{bit:02d}", f"y{bit:02d}",f"z{bit:02d}"
    for w in list(wires.keys()):
        wires[w] = 0
    prev = bit - 1
    wires[f"x{prev:02d}"] = prevXY[0]
    wires[f"y{prev:02d}"] = prevXY[1]
    wires[x], wires[y] = curXY[0], curXY[1]
    [circuit_tick(gates, wires) for r in range(4)]
    return wires[z] == expected_z

TEST_PATTERN = [((0,0), (0,0), 0), ((0,0), (1,0), 1), ((0,0), (0,1), 1), ((0,0), (1,1), 0), ((1,0), (0,0), 0), ((0,1), (0,0), 0), ((1,0), (1,0), 1), ((0,1), (0,1), 1), ((1,1), (0,0), 1), ((1,1), (1,0), 0), ((1,1), (1,1), 1)]

def bit_errors(wires, gates, bit):
    # print(f'testing bit {bit}')
    return sum([int(not test_adder(wires, gates, bit, p[0], p[1], p[2])) for p in TEST_PATTERN])

def scan_swaps(wires, gates, num_outputs, g1, g2, fewest_errors, best_swap):

    gate_swaps.update({g1[1]: g2[1] , g2[1]: g1[1]})
    errors = sum([bit_errors(wires,gates,i) for i in range(1, num_outputs)])
    # if errors < fewest_errors + 2:
        # print(f'swap {g1[1]}-{g2[1]} has errors {errors}')
    if errors < fewest_errors:
        print(f'swap {g1[1]}-{g2[1]} has fewer errors {errors}')
        fewest_errors = errors
        best_swap = {g1[1]: g2[1] , g2[1]: g1[1]}
    del gate_swaps[g1[1]]
    del gate_swaps[g2[1]]
    return fewest_errors, best_swap

output_wires = lambda wires: {w:k for w,k in wires.items() if w.startswith('z')}
with open('day24/input.txt', 'r') as input:
    lines = [l.strip() for l in input.readlines()]
    wires = { v:int(k) for v,k in [l.split(': ') for l in lines if ':' in l]}
    gates = [(ggg[0].split(' '), ggg[1]) for ggg in [l.split(' -> ') for l in lines[len(wires)+1:]]]
    num_outputs = len([g[1] for g in gates if g[1].startswith('z')])

    while len(output_wires(wires)) < num_outputs:
        circuit_tick(gates, wires)
    output_bits = [wires[z] for z in sorted(output_wires(wires).keys(), reverse=True)]
    output_int = int(''.join([str(x) for x in output_bits]),2)

    print(f'PART1: output bits as integer {output_int}')

    # reduce ANDs and ORs to reflective names:
    and1_list, and2_list, xor1_list, xor2_list, or_list = [], [], [], [], []
    for g in gates:
        (left, op, right), output = g[0], g[1]
        xarg = left if left.startswith('x') else right if right.startswith('x') else None
        if op == 'AND':
            if xarg:
                and1_list.append((xarg, output))
            else:
                and2_list.append(((left,right), output))
        elif op == 'XOR':
            if xarg:
                xor1_list.append((xarg, output))
            else:
                xor2_list.append(((left,right), output))
        else:
            or_list.append(((left,right), output))
    and1_list.sort(key = lambda r: r[0])
    xor1_list.sort(key = lambda r: r[0])
    and2_list.sort(key = lambda r: r[1])
    xor2_list.sort(key = lambda r: r[1])
    or_list.sort(key = lambda r: r[1])


    # RULE: AND1 output should not be zXX
    #
    # reveals error in gate 261: y06 AND x06 -> z06
    
    # RULE: AND1 output should be followed by an OR
    #
    # reveals error in gate 264: y25 AND x25 -> tnt
    #    analysis: tnt AND nbs -> vhp
    #    y25 AND x25 -> tnt  
    #    should have led to an input of XOR -> z26, 
    #       (khj XOR mbh -> z26        --------------> swap (tnt,khj)

    # RULE: XOR1 output should not be zXX
    #
    # reveals -

    # RULE: XOR2 output should be zXX
    # reveals error in gate 96: swj XOR rjv -> hwk
    #    analysis: tcn OR jsd -> swj
    #              y06 XOR x06 -> rjv
    #    result: correct output is z06 --------------> SWAP (hwk, z06)
    #
    # reveals error in gate 193: gqc XOR vqv -> cgr
    #    analysis: ksr OR jvs -> gqc
    #              x37 XOR y37 -> vqv
    #    result: correct output is z37 --------------> SWAP (cgr, z37)
    # 
    # reveals error in gate 297: vkh XOR dtq -> hpc  
    #    analysis: y31 XOR x31 -> vkh
    #              vkh XOR dtq -> hpc --------------> SWAP (hpc, z31)
    
    # RULE: AND2 output should not be zXX
    # reveals error in gate 241: gqc AND vqv -> z37
    #    analysis: ksr OR jvs -> gqc
    #              x37 XOR y37 -> vqv --------------> SWAP (z37, cgr) 
    #       should lead to a wire which is the input of an or, whose other input is x37 XOR y37 (vbq), a.k.a cgr

    # RULE: OR output should not be zXX
    # reveals error in gate 292: mjr OR hgw -> z31
    #    analysis: dtq AND vkh -> mjr
    #              y31 AND x31 -> hgw --------------> SWAP (z31, hpc)
    #    should lead to a wire which is XOR and feeds z32 (hpc XOR qrw -> z32)
    #    since qrw is correctly XOR-32, swap with hpc
    #
    #
    # reveals error in gate 124: rgn OR mfp -> z45
    #    analysis: qnw AND spm -> rgn, x44 XOR y44 -> spm
    #              x44 AND y44 -> mfp
    #    THIS IS FINE!

    print(f'PART2: based on manual analysis (!), result is cgr,hpc,hwk,qmd,tnt,z06,z31,z37')


    # in this alternative approach, I tried to programmatically search for pairs which reduced the errors space:
    #
    # gate_swaps = {
    #     'z06': 'hwk', 'hwk': 'z06',
    #     'z37': 'cgr', 'cgr': 'z37', 
    #     'z31': 'hpc', 'hpc': 'z31',
    #     'qmd': 'tnt', 'tnt': 'qmd',
    # }
    # best_swap = {}
    # errors = [bit_errors(wires,gates,i) for i in range(1, num_outputs)]
    # fewest_errors = sum(errors)
    # print(f'without swaps, number of errors={fewest_errors}')
    # for g1_ix, g1 in enumerate(gates):
    #     print(f'scanning swaps for {g1[1]}')
    #     for g2_ix in range(g1_ix+1, len(gates)):
    #         g2 = gates[g2_ix]
    #         if g1[1] in gate_swaps or g2[1] in gate_swaps:
    #             continue
    #         fewest_errors, best_swap = scan_swaps(wires, gates, num_outputs, g1, g2, fewest_errors, best_swap)
    # print(f'first scan errors is {fewest_errors} adopting swap {best_swap}')
