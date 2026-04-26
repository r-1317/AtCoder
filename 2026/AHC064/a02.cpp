#include <algorithm>
#include <chrono>
#include <cmath>
#include <iostream>
#include <random>
#include <set>
#include <tuple>
#include <vector>

using namespace std;

static constexpr double SA_TIME = 0.01;
static constexpr double SA_COOLING = 0.995;
static constexpr double SA_START_TEMP = 2.5;
static constexpr double SA_END_TEMP = 0.01;

struct Op {
	int type;
	int i;
	int j;
	int k;
};

struct Candidate {
	int i;
	int j;
	Op payload;
};

bool is_valid_pairs(const vector<pair<int, int>>& pairs) {
	set<int> dep_used;
	set<int> sid_used;
	for (const auto& [i, j] : pairs) {
		if (dep_used.count(i) || sid_used.count(j)) {
			return false;
		}
		dep_used.insert(i);
		sid_used.insert(j);
	}

	vector<pair<int, int>> pairs_sorted = pairs;
	sort(pairs_sorted.begin(), pairs_sorted.end());
	for (size_t idx = 0; idx + 1 < pairs_sorted.size(); ++idx) {
		if (!(pairs_sorted[idx].second < pairs_sorted[idx + 1].second)) {
			return false;
		}
	}
	return true;
}

int greedy_initial_mask(const vector<Candidate>& candidates) {
	vector<int> order(candidates.size());
	for (int idx = 0; idx < static_cast<int>(candidates.size()); ++idx) {
		order[idx] = idx;
	}
	sort(order.begin(), order.end(), [&](int a, int b) {
		if (candidates[a].i != candidates[b].i) {
			return candidates[a].i < candidates[b].i;
		}
		return candidates[a].j < candidates[b].j;
	});

	int mask = 0;
	int last_j = -1;
	set<int> used_i;
	set<int> used_j;
	for (int idx : order) {
		int i = candidates[idx].i;
		int j = candidates[idx].j;
		if (used_i.count(i) || used_j.count(j)) {
			continue;
		}
		if (j <= last_j) {
			continue;
		}
		mask |= (1 << idx);
		used_i.insert(i);
		used_j.insert(j);
		last_j = j;
	}
	return mask;
}

int evaluate_mask(int mask, const vector<Candidate>& candidates) {
	vector<pair<int, int>> pairs;
	int cnt = 0;
	for (int idx = 0; idx < static_cast<int>(candidates.size()); ++idx) {
		if ((mask >> idx) & 1) {
			pairs.emplace_back(candidates[idx].i, candidates[idx].j);
			cnt += 1;
		}
	}
	if (cnt == 0) {
		return -1000000000;
	}
	if (!is_valid_pairs(pairs)) {
		return -1000000 + cnt;
	}
	return cnt;
}

vector<Op> sa_select(const vector<Candidate>& candidates, mt19937& rng, double time_budget) {
	int n = static_cast<int>(candidates.size());
	if (n == 1) {
		return {candidates[0].payload};
	}

	uniform_real_distribution<double> real_dist(0.0, 1.0);
	uniform_int_distribution<int> bit_dist(0, n - 1);

	int cur_mask = greedy_initial_mask(candidates);
	if (cur_mask == 0) {
		cur_mask = (1 << bit_dist(rng));
	}

	int cur_score = evaluate_mask(cur_mask, candidates);
	int best_mask = cur_mask;
	int best_score = cur_score;

	double temp = SA_START_TEMP;
	const auto start = chrono::steady_clock::now();

	while (true) {
		auto now = chrono::steady_clock::now();
		double elapsed = chrono::duration_cast<chrono::duration<double>>(now - start).count();
		if (elapsed >= time_budget) {
			break;
		}

		int bit = (1 << bit_dist(rng));
		int nxt_mask = cur_mask ^ bit;
		int nxt_score = evaluate_mask(nxt_mask, candidates);

		int diff = nxt_score - cur_score;
		if (diff >= 0) {
			cur_mask = nxt_mask;
			cur_score = nxt_score;
		} else {
			double prob = exp(static_cast<double>(diff) / max(temp, 1e-9));
			if (real_dist(rng) < prob) {
				cur_mask = nxt_mask;
				cur_score = nxt_score;
			}
		}

		if (cur_score > best_score) {
			best_score = cur_score;
			best_mask = cur_mask;
		}

		temp = max(SA_END_TEMP, temp * SA_COOLING);
	}

	vector<Op> selected;
	for (int idx = 0; idx < static_cast<int>(candidates.size()); ++idx) {
		if ((best_mask >> idx) & 1) {
			selected.push_back(candidates[idx].payload);
		}
	}

	if (selected.empty()) {
		selected.push_back(candidates[0].payload);
	}

	vector<pair<int, int>> pairs;
	pairs.reserve(selected.size());
	for (const auto& op : selected) {
		pairs.emplace_back(op.i, op.j);
	}
	if (!is_valid_pairs(pairs)) {
		selected = {candidates[0].payload};
	}

	sort(selected.begin(), selected.end(), [](const Op& a, const Op& b) {
		if (a.i != b.i) {
			return a.i < b.i;
		}
		return a.j < b.j;
	});
	return selected;
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	mt19937 rng(1317);

	int r;
	cin >> r;
	vector<vector<int>> departures(r, vector<int>(10));
	for (int i = 0; i < r; ++i) {
		for (int j = 0; j < 10; ++j) {
			cin >> departures[i][j];
		}
	}
	vector<vector<int>> sidings(r);
	vector<vector<Op>> turns;

	vector<Op> first_turn;
	first_turn.reserve(r);
	for (int i = 0; i < r; ++i) {
		int k = static_cast<int>(departures[i].size());
		vector<int> moved = departures[i];
		departures[i].clear();
		vector<int> new_siding;
		new_siding.reserve(moved.size() + sidings[i].size());
		new_siding.insert(new_siding.end(), moved.begin(), moved.end());
		new_siding.insert(new_siding.end(), sidings[i].begin(), sidings[i].end());
		sidings[i].swap(new_siding);
		first_turn.push_back({0, i, i, k});
	}
	turns.push_back(first_turn);

	while (true) {
		int remaining = 0;
		for (int j = 0; j < r; ++j) {
			remaining += static_cast<int>(sidings[j].size());
		}
		if (remaining == 0) {
			break;
		}

		vector<Candidate> candidates;
		for (int j = 0; j < r; ++j) {
			if (!sidings[j].empty()) {
				int car = sidings[j][0];
				int i = car / 10;
				candidates.push_back({i, j, {1, i, j, 1}});
			}
		}

		vector<Op> ops = sa_select(candidates, rng, SA_TIME);
		turns.push_back(ops);

		for (const auto& op : ops) {
			int i = op.i;
			int j = op.j;
			int car = sidings[j][0];
			sidings[j].erase(sidings[j].begin());
			departures[i].push_back(car);
		}
	}

	while (true) {
		int remaining = 0;
		for (int i = 0; i < r; ++i) {
			remaining += static_cast<int>(departures[i].size());
		}
		if (remaining == 0) {
			break;
		}

		vector<Candidate> candidates;
		for (int i = 0; i < r; ++i) {
			if (!departures[i].empty()) {
				int car = departures[i].back();
				int j = car % 10;
				candidates.push_back({i, j, {0, i, j, 1}});
			}
		}

		vector<Op> ops = sa_select(candidates, rng, SA_TIME);
		turns.push_back(ops);

		for (const auto& op : ops) {
			int i = op.i;
			int j = op.j;
			int car = departures[i].back();
			departures[i].pop_back();
			sidings[j].insert(sidings[j].begin(), car);
		}
	}

	for (int j = 0; j < r; ++j) {
		while (!sidings[j].empty()) {
			int car = sidings[j][0];
			sidings[j].erase(sidings[j].begin());
			int i = car / 10;
			departures[i].push_back(car);
			turns.push_back({{1, i, j, 1}});
		}
	}

	cout << turns.size() << '\n';
	for (const auto& ops : turns) {
		cout << ops.size() << '\n';
		for (const auto& op : ops) {
			cout << op.type << ' ' << op.i << ' ' << op.j << ' ' << op.k << '\n';
		}
	}

	return 0;
}
