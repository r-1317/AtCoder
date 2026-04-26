#include <bits/stdc++.h>
using namespace std;

constexpr double SA_TIME = 0.017;
constexpr double SA_COOLING = 0.995;
constexpr double SA_START_TEMP = 2.5;
constexpr double SA_END_TEMP = 0.01;

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
	for (auto [i, j] : pairs) {
		if (dep_used.count(i) || sid_used.count(j)) {
			return false;
		}
		dep_used.insert(i);
		sid_used.insert(j);
	}

	vector<pair<int, int>> pairs_sorted = pairs;
	sort(pairs_sorted.begin(), pairs_sorted.end());
	for (int idx = 0; idx + 1 < static_cast<int>(pairs_sorted.size()); ++idx) {
		if (!(pairs_sorted[idx].second < pairs_sorted[idx + 1].second)) {
			return false;
		}
	}
	return true;
}

int greedy_initial_mask(const vector<Candidate>& candidates) {
	vector<int> order(candidates.size());
	iota(order.begin(), order.end(), 0);
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

int evaluate_mask(int mask, const vector<Candidate>& candidates, const vector<char>& force_indices) {
	vector<pair<int, int>> pairs;
	int cnt = 0;
	bool has_forced = false;
	for (int idx = 0; idx < static_cast<int>(candidates.size()); ++idx) {
		if ((mask >> idx) & 1) {
			pairs.emplace_back(candidates[idx].i, candidates[idx].j);
			++cnt;
			if (force_indices[idx]) {
				has_forced = true;
			}
		}
	}
	if (cnt == 0) {
		return -1000000000;
	}
	if (!has_forced) {
		return -100000000 + cnt;
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

	int max_dist = 0;
	for (const auto& c : candidates) {
		max_dist = max(max_dist, abs(c.i - c.j));
	}

	vector<char> force_indices(n, 0);
	int first_force = -1;
	for (int idx = 0; idx < n; ++idx) {
		if (abs(candidates[idx].i - candidates[idx].j) == max_dist) {
			force_indices[idx] = 1;
			if (first_force == -1) {
				first_force = idx;
			}
		}
	}

	uniform_int_distribution<int> bit_dist(0, n - 1);
	uniform_real_distribution<double> prob_dist(0.0, 1.0);

	int cur_mask = greedy_initial_mask(candidates);
	if (cur_mask == 0) {
		cur_mask = (1 << bit_dist(rng));
	}

	bool has_forced_in_cur = false;
	for (int idx = 0; idx < n; ++idx) {
		if (((cur_mask >> idx) & 1) && force_indices[idx]) {
			has_forced_in_cur = true;
			break;
		}
	}
	if (!has_forced_in_cur && first_force != -1) {
		cur_mask |= (1 << first_force);
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

		int bit = (1 << bit_dist(rng));
		int nxt_mask = cur_mask ^ bit;
		int nxt_score = evaluate_mask(nxt_mask, candidates, force_indices);

		int diff = nxt_score - cur_score;
		if (diff >= 0) {
			cur_mask = nxt_mask;
			cur_score = nxt_score;
		} else {
			double prob = exp(static_cast<double>(diff) / max(temp, 1e-9));
			if (prob_dist(rng) < prob) {
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
	vector<int> selected_indices;
	for (int idx = 0; idx < n; ++idx) {
		if ((best_mask >> idx) & 1) {
			selected.push_back(candidates[idx].payload);
			selected_indices.push_back(idx);
		}
	}

	if (selected.empty() && first_force != -1) {
		selected = {candidates[first_force].payload};
		selected_indices = {first_force};
	}

	bool has_forced_in_selected = false;
	for (int idx : selected_indices) {
		if (force_indices[idx]) {
			has_forced_in_selected = true;
			break;
		}
	}
	if (!has_forced_in_selected && first_force != -1) {
		selected = {candidates[first_force].payload};
	}

	vector<pair<int, int>> pairs;
	for (const auto& op : selected) {
		pairs.emplace_back(op.i, op.j);
	}
	if (!is_valid_pairs(pairs) && first_force != -1) {
		selected = {candidates[first_force].payload};
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
		for (int c = 0; c < 10; ++c) {
			cin >> departures[i][c];
		}
	}
	vector<vector<int>> sidings(r);

	vector<vector<Op>> turns;

	vector<Op> first_turn;
	for (int i = 0; i < r; ++i) {
		int k = static_cast<int>(departures[i].size());
		vector<int> moved = departures[i];
		departures[i].clear();
		sidings[i].insert(sidings[i].begin(), moved.begin(), moved.end());
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
		for (const auto& d : departures) {
			remaining += static_cast<int>(d.size());
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
