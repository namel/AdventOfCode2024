import math

# program is sequence of opcode/operand
# operands can be literal
# operands can be combo (lit: 0-3, 4:RegisterA, 5: RegisterB, 6: RegisterC)
#
# opcode 0=adv= RegA/(2^combo); truncate; write to A
# opcode 1=bxl= XOR(RegB,literal); write to B

get_combo = lambda operand, registers: operand if operand < 4 else registers[operand - 4]

def execute(op_ptr, program, registers, output, i):
    instruction, operand, combo = program[op_ptr], program[op_ptr+1], get_combo(program[op_ptr+1], registers)
    op_ptr += 2
    if instruction == 0:
        registers[0] = math.trunc(registers[0] / math.pow(2, combo))
    elif instruction == 1:
        registers[1] = registers[1] ^ operand
    elif instruction == 2:
        registers[1] = combo % 8
    elif instruction == 3:
        if registers[0] > 0:
            op_ptr = operand
    elif instruction == 4:
        registers[1] = registers[1] ^ registers[2]
    elif instruction == 5:
        output.append(combo % 8)
        if program[:len(output)] != output:
            return 1000
        if len(output) > 14:
            print(f'at step {i} program is {output}')
    elif instruction == 6:
        registers[1] = math.trunc(registers[0] / math.pow(2, combo))
    elif instruction == 7:
        registers[2] = math.trunc(registers[0] / math.pow(2, combo))
    return op_ptr


with open('day17/input.txt', 'r') as input:
    lines = [l.strip() for l in input.readlines()]
    registers = [int(l.split(':')[1].strip()) for l in lines[0:len(lines)-2]]
    program = [int(el) for el in lines[len(lines)-1].split(':')[1].strip().split(',')]
    op_ptr, output = 0, []

    while op_ptr < len(program):
        op_ptr = execute(op_ptr, program, registers, output, 0)
    msg = ','.join([str(n) for n in output])
    print(f'PART1: {msg}')

    i = 10000767485
    while True:
        op_ptr, output = 0, []
        registers = [i, 0, 0]
        while op_ptr < len(program):
            op_ptr = execute(op_ptr, program, registers, output, i)
        if i % 1000000000 == 0:
            print(i)
        if output == program:
            print(f'PART2: program outputs self at RegA {i}')
            break
        i += 4194304 # This was discovered when I observed regular interval jumps at length 5
    

    