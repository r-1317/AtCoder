#include <bits/stdc++.h>
using namespace std;

// 定数（問題条件で固定）
static const int N = 100;
static const int K = 10;
static const int T = 10000;

// 方針03用
static const double P = 0.02;       // 木を赤化する確率
static const double TIME_LIMIT = 1.99; // 秒

// シミュレーションしてスコア計算（Pythonの calc_score 相当）
long long calc_score(const vector<int>& outputs) {
    vector<char> red(N, 0); // 木の赤化状態（ショップは無視）
    vector<unordered_set<string>> inventories(K);

    int pos = 0;
    bool has_prev_move_from = false;
    int prev_move_from = -1;
    string cone;  // 手元のコーン（味列）

    for (int out : outputs) {
        if (out == -1) {
            // 行動2: 現在位置が白い木のときのみ可
            if (!(K <= pos && pos < N) || red[pos]) return -(long long)1e18;
            red[pos] = 1;
            continue;
        }

        int v = out;
        if (!(0 <= v && v < N)) return -(long long)1e18;
        if (has_prev_move_from && v == prev_move_from) return -(long long)1e18;

        prev_move_from = pos;
        has_prev_move_from = true;
        pos = v;

        if (pos < K) {
            inventories[pos].insert(cone);
            cone.clear();
        } else {
            cone.push_back(red[pos] ? 'R' : 'W');
        }
    }

    long long sum = 0;
    for (int i = 0; i < K; i++) sum += (long long)inventories[i].size();
    return sum;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int Nin, M, Kin, Tin;
    cin >> Nin >> M >> Kin >> Tin; // N,K,Tは固定だが入力として来るので読む（無視してOK）

    vector<vector<int>> adj(N);
    for (int i = 0; i < M; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    // 座標入力（この解では使わない）
    // Python版はK行だけ読むが、どちらでもOK。ここでは全部読み捨てしておく。
    for (int i = 0; i < N; i++) {
        int x, y;
        cin >> x >> y;
    }

    // 乱数
    mt19937 rng(1317);
    uniform_real_distribution<double> real01(0.0, 1.0);

    long long max_score = -1;
    vector<int> best_outputs;

    using Clock = chrono::steady_clock;
    auto start = Clock::now();

    auto elapsed_sec = [&]() -> double {
        return chrono::duration<double>(Clock::now() - start).count();
    };

    while (elapsed_sec() < TIME_LIMIT) {
        vector<char> is_red(N, 0);
        vector<int> outputs;
        outputs.reserve(T);

        int current_pos = 0;
        int prev_pos = -1;
        int step_count = 0;

        while (step_count < T) {
            // 次の移動先候補（戻り禁止: prev_pos を除外）
            const auto& nbr = adj[current_pos];
            vector<int> candidates;
            candidates.reserve(nbr.size());
            for (int v : nbr) if (v != prev_pos) candidates.push_back(v);

            // 2-辺連結 & 関節点なし想定なので候補は必ず残る
            uniform_int_distribution<int> pick(0, (int)candidates.size() - 1);
            int next_pos = candidates[pick(rng)];

            outputs.push_back(next_pos);
            prev_pos = current_pos;
            current_pos = next_pos;
            step_count++;

            // 木なら確率で赤化（ただしT手を超えない範囲で）
            if (current_pos >= K && !is_red[current_pos]) {
                if (real01(rng) < P && step_count < T) {
                    is_red[current_pos] = 1;
                    outputs.push_back(-1);
                    step_count++;
                }
            }
        }

        long long score = calc_score(outputs);
        if (score > max_score) {
            max_score = score;
            best_outputs = outputs;
        }
    }

    // 出力
    for (int v : best_outputs) {
        cout << v << '\n';
    }
    return 0;
}
