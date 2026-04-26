#include <algorithm>
#include <chrono>
#include <cmath>
#include <deque>
#include <iostream>
#include <random>
#include <set>
#include <utility>
#include <vector>

using namespace std;

constexpr double SA_TIME = 0.0185;
constexpr double SA_COOLING = 0.995;
constexpr double SA_START_TEMP = 2.5;
constexpr double SA_END_TEMP = 0.01;

struct Operation {
	int type;
	int i;
	int j;
	int k;
};

struct Candidate {
	int i;
	int j;
	Operation payload;
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

	vector<pair<int, int>> sorted_pairs = pairs;
	sort(sorted_pairs.begin(), sorted_pairs.end());
	for (int idx = 0; idx + 1 < static_cast<int>(sorted_pairs.size()); ++idx) {
		if (!(sorted_pairs[idx].second < sorted_pairs[idx + 1].second)) {
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

int evaluate_mask(int mask, const vector<Candidate>& candidates, const set<int>& force_indices) {
	vector<pair<int, int>> pairs;
	int moved = 0;
	bool has_forced = false;

	for (int idx = 0; idx < static_cast<int>(candidates.size()); ++idx) {
		if ((mask >> idx) & 1) {
			pairs.emplace_back(candidates[idx].i, candidates[idx].j);
			moved += candidates[idx].payload.k;
			if (force_indices.count(idx)) {
				has_forced = true;
			}
		}
	}

	if (moved == 0) {
		return -1000000000;
	}
	if (!has_forced) {
		return -100000000 + moved;
	}
	if (!is_valid_pairs(pairs)) {
		return -1000000 + moved;
	}
	return moved;
}

vector<Operation> sa_select(const vector<Candidate>& candidates, mt19937& rng, double time_budget) {
	int n = static_cast<int>(candidates.size());
	if (n == 1) {
		return {candidates[0].payload};
	}

	int max_dist = 0;
	for (const auto& c : candidates) {
		max_dist = max(max_dist, abs(c.i - c.j));
	}

	set<int> force_indices;
	for (int idx = 0; idx < n; ++idx) {
		if (abs(candidates[idx].i - candidates[idx].j) == max_dist) {
			force_indices.insert(idx);
		}
	}

	int cur_mask = greedy_initial_mask(candidates);
	uniform_int_distribution<int> dist(0, n - 1);
	uniform_real_distribution<double> dist01(0.0, 1.0);

	if (cur_mask == 0) {
		cur_mask = (1 << dist(rng));
	}

	bool contains_forced = false;
	for (int idx : force_indices) {
		if ((cur_mask >> idx) & 1) {
			contains_forced = true;
			break;
		}
	}
	if (!contains_forced) {
		int fidx = *force_indices.begin();
		cur_mask |= (1 << fidx);
	}

	int cur_score = evaluate_mask(cur_mask, candidates, force_indices);
	int best_mask = cur_mask;
	int best_score = cur_score;

	double temp = SA_START_TEMP;
	auto start = chrono::steady_clock::now();

	while (true) {
		auto now = chrono::steady_clock::now();
		double elapsed = chrono::duration<double>(now - start).count();
		if (elapsed >= time_budget) {
			break;
		}

		int bit = 1 << dist(rng);
		int nxt_mask = cur_mask ^ bit;
		int nxt_score = evaluate_mask(nxt_mask, candidates, force_indices);

		int diff = nxt_score - cur_score;
		if (diff >= 0) {
			cur_mask = nxt_mask;
			cur_score = nxt_score;
		} else {
			double prob = exp(static_cast<double>(diff) / max(temp, 1e-9));
			if (dist01(rng) < prob) {
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

	vector<Operation> selected;
	vector<int> selected_indices;
	for (int idx = 0; idx < n; ++idx) {
		if ((best_mask >> idx) & 1) {
			selected.push_back(candidates[idx].payload);
			selected_indices.push_back(idx);
		}
	}

	if (selected.empty()) {
		int fidx = *force_indices.begin();
		selected = {candidates[fidx].payload};
		selected_indices = {fidx};
	}

	bool has_forced_selected = false;
	for (int idx : selected_indices) {
		if (force_indices.count(idx)) {
			has_forced_selected = true;
			break;
		}
	}
	if (!has_forced_selected) {
		int fidx = *force_indices.begin();
		selected = {candidates[fidx].payload};
	}

	vector<pair<int, int>> pairs;
	for (const auto& op : selected) {
		pairs.emplace_back(op.i, op.j);
	}
	if (!is_valid_pairs(pairs)) {
		int fidx = *force_indices.begin();
		selected = {candidates[fidx].payload};
	}

	sort(selected.begin(), selected.end(), [](const Operation& a, const Operation& b) {
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

	mt19937 rng(0);

	int r;
	cin >> r;

	vector<vector<int>> departures(r, vector<int>(10));
	for (int i = 0; i < r; ++i) {
		for (int j = 0; j < 10; ++j) {
			cin >> departures[i][j];
		}
	}
	vector<deque<int>> sidings(r);

	vector<vector<Operation>> turns;

	vector<Operation> first_turn;
	first_turn.reserve(r);
	for (int i = 0; i < r; ++i) {
		int k = static_cast<int>(departures[i].size());
		for (int x : departures[i]) {
			sidings[i].push_back(x);
		}
		departures[i].clear();
		first_turn.push_back({0, i, i, k});
	}
	turns.push_back(first_turn);

	while (true) {
		int remaining = 0;
		for (const auto& s : sidings) {
			remaining += static_cast<int>(s.size());
		}
		if (remaining == 0) {
			break;
		}

		vector<Candidate> candidates;
		candidates.reserve(r);
		for (int j = 0; j < r; ++j) {
			if (!sidings[j].empty()) {
				int i = sidings[j][0] / 10;
				int k = 1;
				if (sidings[j].size() >= 2 && sidings[j][1] / 10 == i) {
					k = 2;
				}
				candidates.push_back({i, j, {1, i, j, k}});
			}
		}

		vector<Operation> ops = sa_select(candidates, rng, SA_TIME);
		turns.push_back(ops);

		for (const auto& op : ops) {
			int i = op.i;
			int j = op.j;
			int k = op.k;
			for (int cnt = 0; cnt < k; ++cnt) {
				int car = sidings[j].front();
				sidings[j].pop_front();
				departures[i].push_back(car);
			}
		}
	}

	while (true) {
		int remaining = 0;
		for (const auto& d : departures) {
			remaining += static_cast<int>(d.size());
		}
		if (remaining == 0) {
			break;
		}

		vector<Candidate> candidates;
		candidates.reserve(r);
		for (int i = 0; i < r; ++i) {
			if (!departures[i].empty()) {
				int j = departures[i].back() % 10;
				int k = 1;
				if (departures[i].size() >= 2 && departures[i][departures[i].size() - 2] % 10 == j) {
					k = 2;
				}
				candidates.push_back({i, j, {0, i, j, k}});
			}
		}

		vector<Operation> ops = sa_select(candidates, rng, SA_TIME);
		turns.push_back(ops);

		for (const auto& op : ops) {
			int i = op.i;
			int j = op.j;
			int k = op.k;
			for (int idx = 0; idx < k; ++idx) {
				int car = departures[i].back();
				departures[i].pop_back();
				sidings[j].push_front(car);
			}
		}
	}

	for (int j = 0; j < r; ++j) {
		while (!sidings[j].empty()) {
			int car = sidings[j].front();
			sidings[j].pop_front();
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
