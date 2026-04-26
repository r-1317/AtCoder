import math
import random
import sys
import time


SA_TIME = 0.02
SA_COOLING = 0.995
SA_START_TEMP = 2.5
SA_END_TEMP = 0.01


def is_valid_pairs(pairs):
	dep_used = set()
	sid_used = set()
	for i, j in pairs:
		if i in dep_used or j in sid_used:
			return False
		dep_used.add(i)
		sid_used.add(j)

	pairs_sorted = sorted(pairs)
	for idx in range(len(pairs_sorted) - 1):
		if not (pairs_sorted[idx][1] < pairs_sorted[idx + 1][1]):
			return False
	return True


def greedy_initial_mask(candidates):
	# candidates: [(i, j, payload), ...]
	order = sorted(range(len(candidates)), key=lambda x: (candidates[x][0], candidates[x][1]))
	mask = 0
	last_j = -1
	used_i = set()
	used_j = set()
	for idx in order:
		i, j, _ = candidates[idx]
		if i in used_i or j in used_j:
			continue
		if j <= last_j:
			continue
		mask |= 1 << idx
		used_i.add(i)
		used_j.add(j)
		last_j = j
	return mask


def evaluate_mask(mask, candidates, force_indices):
	pairs = []
	cnt = 0
	has_forced = False
	for idx, (i, j, _) in enumerate(candidates):
		if (mask >> idx) & 1:
			pairs.append((i, j))
			cnt += 1
			if idx in force_indices:
				has_forced = True
	if cnt == 0:
		return -10**9
	if not has_forced:
		return -10**8 + cnt
	if not is_valid_pairs(pairs):
		return -10**6 + cnt
	return cnt


def sa_select(candidates, rng, time_budget):
	n = len(candidates)
	if n == 1:
		return [candidates[0][2]]

	# Must include at least one candidate with maximum |i-j|.
	max_dist = max(abs(i - j) for i, j, _ in candidates)
	force_indices = {idx for idx, (i, j, _) in enumerate(candidates) if abs(i - j) == max_dist}

	cur_mask = greedy_initial_mask(candidates)
	if cur_mask == 0:
		cur_mask = 1 << rng.randrange(n)

	# Ensure initial mask contains a forced candidate.
	if not any(((cur_mask >> idx) & 1) for idx in force_indices):
		fidx = next(iter(force_indices))
		cur_mask |= 1 << fidx

	cur_score = evaluate_mask(cur_mask, candidates, force_indices)
	best_mask = cur_mask
	best_score = cur_score

	temp = SA_START_TEMP
	start = time.perf_counter()

	while time.perf_counter() - start < time_budget:
		bit = 1 << rng.randrange(n)
		nxt_mask = cur_mask ^ bit
		nxt_score = evaluate_mask(nxt_mask, candidates, force_indices)

		diff = nxt_score - cur_score
		if diff >= 0:
			cur_mask = nxt_mask
			cur_score = nxt_score
		else:
			prob = math.exp(diff / max(temp, 1e-9))
			if rng.random() < prob:
				cur_mask = nxt_mask
				cur_score = nxt_score

		if cur_score > best_score:
			best_score = cur_score
			best_mask = cur_mask

		temp = max(SA_END_TEMP, temp * SA_COOLING)

	selected = []
	selected_indices = []
	for idx, (_, _, payload) in enumerate(candidates):
		if (best_mask >> idx) & 1:
			selected.append(payload)
			selected_indices.append(idx)

	if not selected:
		fidx = next(iter(force_indices))
		selected = [candidates[fidx][2]]
		selected_indices = [fidx]

	# If SA result misses forced candidate, force one move this turn.
	if all(idx not in force_indices for idx in selected_indices):
		fidx = next(iter(force_indices))
		selected = [candidates[fidx][2]]

	# Validity guard.
	pairs = [(op[1], op[2]) for op in selected]
	if not is_valid_pairs(pairs):
		fidx = next(iter(force_indices))
		selected = [candidates[fidx][2]]

	selected.sort(key=lambda op: (op[1], op[2]))
	return selected


def main() -> None:
	input = sys.stdin.readline
	rng = random.Random(0)

	r = int(input())
	departures = [list(map(int, input().split())) for _ in range(r)]
	sidings = [[] for _ in range(r)]

	turns = []

	# 1) Same as a01/a02: departure i -> siding i, all in one turn.
	first_turn = []
	for i in range(r):
		k = len(departures[i])
		moved = departures[i][-k:]
		departures[i] = departures[i][:-k]
		sidings[i] = moved + sidings[i]
		first_turn.append((0, i, i, k))
	turns.append(first_turn)

	# 2) Move from sidings to appropriate departures (by tens digit), in parallel using SA.
	while True:
		remaining = sum(len(s) for s in sidings)
		if remaining == 0:
			break

		candidates = []
		for j in range(r):
			if sidings[j]:
				car = sidings[j][0]
				i = car // 10
				candidates.append((i, j, (1, i, j, 1)))

		ops = sa_select(candidates, rng, SA_TIME)
		turns.append(ops)

		for _, i, j, k in ops:
			_ = k
			car = sidings[j][0]
			sidings[j] = sidings[j][1:]
			departures[i].append(car)

	# 3) Move departures -> sidings by ones digit, in parallel using SA.
	while True:
		remaining = sum(len(d) for d in departures)
		if remaining == 0:
			break

		candidates = []
		for i in range(r):
			if departures[i]:
				car = departures[i][-1]
				j = car % 10
				candidates.append((i, j, (0, i, j, 1)))

		ops = sa_select(candidates, rng, SA_TIME)
		turns.append(ops)

		for _, i, j, k in ops:
			_ = k
			car = departures[i].pop()
			sidings[j] = [car] + sidings[j]

	# 4) Sequentially move one car at a time from siding 0..9 to appropriate departure.
	for j in range(r):
		while sidings[j]:
			car = sidings[j][0]
			sidings[j] = sidings[j][1:]
			i = car // 10
			departures[i].append(car)
			turns.append([(1, i, j, 1)])

	print(len(turns))
	for ops in turns:
		print(len(ops))
		for t, i, j, k in ops:
			print(t, i, j, k)


if __name__ == "__main__":
	main()
