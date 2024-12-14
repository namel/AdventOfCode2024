from collections import defaultdict
from functools import reduce

dist, similarity_score = 0, 0
with open('./day1/input.txt', 'r') as input:

    # calculate distances between pairs of items
    data = [line.strip().split('   ') for line in input.readlines()]
    list1 = [int(d[0]) for d in data]
    list1.sort()
    list2 = [int(d[1]) for d in data]
    list2.sort()
    for i in range(0, len(list1)):
        dist += abs(list1[i] - list2[i])
    
    key_counts = defaultdict(int)

    # create a lookup of counts and then reduce as you scan
    for k in list2:
        key_counts[k] += 1
    similarity_score = reduce(lambda acc, el: acc + el * key_counts[el], list1, 0)

print(f"distance is: {dist}")
print(f"similarity is: {similarity_score}")