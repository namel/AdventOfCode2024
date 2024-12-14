from collections import namedtuple
from functools import reduce

block_id = lambda block_ix: block_ix/2
get_file_id = lambda block_ix: block_ix/2 if (block_ix % 2 == 0) else None
checksum_of_range = lambda id, start, length: (id or 0) * sum(range(start, start + length))
Range = namedtuple('Range', ['start', 'len', 'id'])

with open('day9/input.txt', 'r') as input:
    disk_layout = []
    map = input.read()
    [disk_layout.append(int(c)) for c in map]
    block_pos, block_ix, end_block_ix, checksum = 0, 0, len(map) - 1, 0

    # part 1: fine-grained file moves
    while disk_layout[block_ix]>0:

        # filled range: add pre-existing blocks to checksum
        checksum += checksum_of_range(block_id(block_ix), block_pos, int(disk_layout[block_ix]))
        block_pos += disk_layout[block_ix]

        # empty range: collect end-range blocks to checksum
        for j in range(0, disk_layout[block_ix+1]):
            while end_block_ix > (block_ix + 1) and (disk_layout[end_block_ix]) == 0:
                end_block_ix -= 2
            if end_block_ix > (block_ix + 1):
                checksum += block_id(end_block_ix) * block_pos
                block_pos += 1
                disk_layout[end_block_ix] -= 1
        block_ix += 2

    # part 2: contiguous file moves
    ranges, pos = [], 0
    for range_ix in range(len(map)):
        ranges.append(Range(pos, int(map[range_ix]), get_file_id(range_ix))) # range => (start, len, id)
        pos += int(map[range_ix])
    for candidate_ix in range(range_ix, -1, -1):
        candidate = ranges[candidate_ix]
        if candidate.id == None:
            continue
        free_range_ix = 1
        while free_range_ix < candidate_ix:
            free_range = ranges[free_range_ix]
            if free_range.id == None and free_range.len >= candidate.len:
                new_range = Range(free_range.start, candidate.len, candidate.id)
                reduced_free_range = [Range(free_range.start + candidate.len, free_range.len - candidate.len, None)] if free_range.len > candidate.len else []
                ranges[candidate_ix] = Range(candidate.start, candidate.len, None)
                ranges = ranges[:free_range_ix] + [new_range] + reduced_free_range + ranges[free_range_ix+1:]
                break
            free_range_ix += 1

    part2_checksum = reduce(lambda acc, el: acc + checksum_of_range(el.id, el.start, el.len), ranges, 0)
    print(f"PART1: checksum = {checksum}")
    print(f"PART2: checksum = {part2_checksum}")
