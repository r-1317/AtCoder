#include <algorithm>
#include <chrono>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

using namespace std;

constexpr int K = 700;
constexpr double TIME_LIMIT = 1.9;

struct BeamState {
	vector<int> pos;
	vector<int> col;
	vector<int> foods;
	int matches;
	int score;
	int node_id;
};

int score_of(int length, int matches, int turns) {
	return 10000 * (length + matches) - turns;
}

vector<char> reconstruct_ops(const vector<int>& parents, const vector<char>& moves, int node_id) {
	vector<char> ops;
	int cur = node_id;
	while (cur > 0) {
		ops.push_back(moves[cur]);
		cur = parents[cur];
	}
	reverse(ops.begin(), ops.end());
	return ops;
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int N, M, C;
	cin >> N >> M >> C;

	vector<int> desired(M);
	for (int i = 0; i < M; ++i) {
		cin >> desired[i];
	}

	vector<int> board(N * N, 0);
	for (int i = 0; i < N; ++i) {
		const int base = i * N;
		for (int j = 0; j < N; ++j) {
			cin >> board[base + j];
		}
	}

	const vector<tuple<int, int, char>> dirs = {
			{-1, 0, 'U'},
			{1, 0, 'D'},
			{0, -1, 'L'},
			{0, 1, 'R'},
	};

	vector<vector<pair<int, char>>> neighbors(N * N);
	for (int r = 0; r < N; ++r) {
		for (int c = 0; c < N; ++c) {
			const int idx = r * N + c;
			vector<pair<int, char>> cand;
			for (const auto& [dr, dc, ch] : dirs) {
				const int nr = r + dr;
				const int nc = c + dc;
				if (0 <= nr && nr < N && 0 <= nc && nc < N) {
					cand.emplace_back(nr * N + nc, ch);
				}
			}
			neighbors[idx] = move(cand);
		}
	}

	vector<int> init_pos = {4 * N, 3 * N, 2 * N, 1 * N, 0};
	vector<int> init_col = {1, 1, 1, 1, 1};
	vector<int> init_foods = board;
	const int init_matches = 5;
	const int init_score = score_of(5, 5, 0);

	vector<int> parents;
	parents.push_back(-1);
	vector<char> moves;
	moves.push_back('\0');

	vector<BeamState> beam;
	beam.push_back(BeamState{init_pos, init_col, init_foods, init_matches, init_score, 0});

	int best_node = 0;
	int best_score = init_score;
	int best_len = 5;
	int best_matches = 5;
	int best_turn = 0;
	int turn = 0;

	const auto start_time = chrono::steady_clock::now();

	while (!beam.empty()) {
		const auto now = chrono::steady_clock::now();
		const double elapsed = chrono::duration<double>(now - start_time).count();
		if (elapsed >= TIME_LIMIT) {
			break;
		}

		struct NextCand {
			int score;
			int node_id;
			vector<int> pos;
			vector<int> col;
			vector<int> foods;
			int matches;
		};

		vector<NextCand> next_cands;
		const int next_turn = turn + 1;

		for (const auto& st : beam) {
			const vector<int>& pos = st.pos;
			const vector<int>& col = st.col;
			const vector<int>& foods = st.foods;
			const int k = static_cast<int>(col.size());
			const int head = pos[0];
			const int neck = pos[1];

			for (const auto& [nh, mv] : neighbors[head]) {
				if (nh == neck) {
					continue;
				}

				vector<int> moved_pos;
				moved_pos.reserve(k);
				moved_pos.push_back(nh);
				moved_pos.insert(moved_pos.end(), pos.begin(), pos.end() - 1);

				const int food_color = foods[nh];

				vector<int> new_pos;
				vector<int> new_col;
				vector<int> new_foods;
				int new_matches = st.matches;

				if (food_color != 0) {
					// Eat first; this turn never includes biting by problem statement.
					new_foods = foods;
					new_foods[nh] = 0;

					new_pos.reserve(k + 1);
					new_pos.push_back(nh);
					new_pos.insert(new_pos.end(), pos.begin(), pos.end());

					new_col.reserve(k + 1);
					new_col.insert(new_col.end(), col.begin(), col.end());
					new_col.push_back(food_color);

					if (k < M && food_color == desired[k]) {
						++new_matches;
					}
				} else {
					int bite_h = -1;
					for (int h = 1; h <= k - 2; ++h) {
						if (moved_pos[h] == nh) {
							bite_h = h;
							break;
						}
					}

					if (bite_h != -1) {
						new_pos.assign(moved_pos.begin(), moved_pos.begin() + bite_h + 1);
						new_col.assign(col.begin(), col.begin() + bite_h + 1);

						new_foods = foods;
						for (int p = bite_h + 1; p < k; ++p) {
							new_foods[moved_pos[p]] = col[p];
						}

						const int upto = min(static_cast<int>(new_col.size()), M);
						int mcnt = 0;
						for (int i = 0; i < upto; ++i) {
							if (new_col[i] == desired[i]) {
								++mcnt;
							}
						}
						new_matches = mcnt;
					} else {
						new_pos = move(moved_pos);
						new_col = col;
						new_foods = foods;
					}
				}

				const int new_len = static_cast<int>(new_col.size());
				const int new_score = score_of(new_len, new_matches, next_turn);

				const int node_id = static_cast<int>(parents.size());
				parents.push_back(st.node_id);
				moves.push_back(mv);

				if (new_score > best_score) {
					best_score = new_score;
					best_node = node_id;
					best_len = new_len;
					best_matches = new_matches;
					best_turn = next_turn;
				}

				next_cands.push_back(NextCand{new_score, node_id, move(new_pos), move(new_col), move(new_foods), new_matches});
			}
		}

		if (next_cands.empty()) {
			break;
		}

		sort(next_cands.begin(), next_cands.end(), [](const NextCand& a, const NextCand& b) {
			return a.score > b.score;
		});

		if (static_cast<int>(next_cands.size()) > K) {
			next_cands.resize(K);
		}

		beam.clear();
		beam.reserve(next_cands.size());
		for (auto& cand : next_cands) {
			beam.push_back(BeamState{move(cand.pos), move(cand.col), move(cand.foods), cand.matches, cand.score, cand.node_id});
		}

		turn = next_turn;
	}

	const vector<char> ans = reconstruct_ops(parents, moves, best_node);
	for (char c : ans) {
		cout << c << '\n';
	}

	const long long absolute_score = static_cast<long long>(best_turn)
		+ 10000LL * (static_cast<long long>(best_len - best_matches) + 2LL * (M - best_len));
	cerr << absolute_score / M << '\n';

	return 0;
}
