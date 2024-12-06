from collections import defaultdict


blocked_predecessors = defaultdict(set)

def confirm_rules(update):
    passed_pages = set()
    for page in update:
        if page in blocked_predecessors and not passed_pages.isdisjoint(blocked_predecessors[page]):
            return False
        passed_pages.add(page)
    return True

def swap_with_next(sequence, ix):
    next_el = sequence[ix+1]
    sequence[ix+1] = sequence[ix]
    sequence[ix] = next_el

allowed_after = lambda page_ix, update: update[page_ix+1] not in blocked_predecessors[update[page_ix]]

def fix_update_done(update):
    passed_pages = set()
    for page_ix, page in enumerate(update):
        if page in blocked_predecessors:
            blocking_pages = passed_pages.intersection(blocked_predecessors[page])
            if len(blocking_pages) > 0:
                bp = blocking_pages.pop()
                blocking_page_ix = update.index(bp)
                while blocking_page_ix < page_ix and allowed_after(blocking_page_ix, update):
                    swap_with_next(update, blocking_page_ix)
                    blocking_page_ix += 1
                while blocking_page_ix < page_ix and allowed_after(page_ix - 1, update):
                    swap_with_next(update, page_ix - 1)
                    page_ix -= 1
                return False
        passed_pages.add(page)
    return True

def fix_update(update):
    print(f"starting to fix {update}")
    update_is_fixed = False
    while not update_is_fixed:
        update_is_fixed = fix_update_done(update)
    return update

with open('day5/input.txt', 'r') as input:
    lines = input.readlines()
    rules = [l.strip().split('|') for l in lines if '|' in l]
    updates = [l.strip().split(',') for l in lines if ',' in l]
    [blocked_predecessors[r[0]].add(r[1]) for r in rules]
    middles_of_valid_updates = [ int(u[len(u)//2]) for u in updates if confirm_rules(u)]
    broken_updates = [u for u in updates if not confirm_rules(u)]
    middles_of_fixed_updates = [int(fix_update(u)[len(u)//2]) for u in broken_updates]
    print(f"PART1: sum of middles of valid updates {sum(middles_of_valid_updates)}")
    print(f"PART2: sum of middles of fixed updates {sum(middles_of_fixed_updates)}")

