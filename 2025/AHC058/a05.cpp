#include <bits/stdc++.h>
#include <boost/multiprecision/cpp_int.hpp>

using namespace std;
using boost::multiprecision::cpp_int;

static constexpr int N = 10;
static constexpr int L = 4;
static constexpr int T = 500;
static constexpr long long K = 1;

// ---- バランス調整パラメータ（ここをチューニングしてください） ----
static constexpr double ALPHA = 0.35; // imbalance へのペナルティ係数（大きいほど均一化を優先）
static constexpr int GAP = 3;         // minUpg + GAP を超える ID の強化は候補から除外（大きいほど緩い）
// ------------------------------------------------------------------

struct State {
    int turn = 0;
    cpp_int apples = 0;

    array<array<cpp_int, N>, L> cnt{};
    array<array<int, N>, L> pw{};

    cpp_int result = 0; // 「これ以降強化なし」の最終りんご予測
    vector<pair<int,int>> actions; // (level, id) or (-1,-1)

    // 追加：機械IDごとの強化回数
    array<int, N> upgCount{};

    static cpp_int predict_result(
        int curTurn,
        const cpp_int& curApples,
        const array<long long, N>& A,
        const array<array<cpp_int, N>, L>& cnt0,
        const array<array<int, N>, L>& pw0
    ) {
        cpp_int apples = curApples;
        auto cnt = cnt0;
        auto pw  = pw0;

        for (int t = curTurn; t < T; t++) {
            for (int j = 0; j < N; j++) {
                if (pw[0][j] != 0) {
                    apples += cpp_int(A[j]) * cnt[0][j] * pw[0][j];
                }
            }
            for (int i = 1; i < L; i++) {
                for (int j = 0; j < N; j++) {
                    if (pw[i][j] != 0) {
                        cnt[i - 1][j] += cnt[i][j] * pw[i][j];
                    }
                }
            }
        }
        return apples;
    }

    void recompute_result(const array<long long, N>& A) {
        result = predict_result(turn, apples, A, cnt, pw);
    }

    bool can_enpower(int machine_id, int level, const array<array<long long, N>, L>& C) const {
        if (machine_id == -1 && level == -1) return true;
        long long base = C[level][machine_id];
        long long mul  = (long long)pw[level][machine_id] + 1;
        cpp_int cost   = cpp_int(base) * mul;
        return apples >= cost;
    }

    bool enpower(int machine_id, int level,
                 const array<array<long long, N>, L>& C,
                 const array<long long, N>& /*A*/) {
        if (machine_id == -1 && level == -1) {
            actions.push_back({-1, -1});
            return true;
        }
        long long base = C[level][machine_id];
        long long mul  = (long long)pw[level][machine_id] + 1;
        cpp_int cost   = cpp_int(base) * mul;

        if (apples >= cost) {
            apples -= cost;
            pw[level][machine_id] += 1;
            upgCount[machine_id] += 1;              // ★追加：ID別強化回数を更新
            actions.push_back({level, machine_id});
            return true;
        }
        return false;
    }

    void step(const array<long long, N>& A) {
        for (int j = 0; j < N; j++) {
            if (pw[0][j] != 0) {
                apples += cpp_int(A[j]) * cnt[0][j] * pw[0][j];
            }
        }
        for (int i = 1; i < L; i++) {
            for (int j = 0; j < N; j++) {
                if (pw[i][j] != 0) {
                    cnt[i - 1][j] += cnt[i][j] * pw[i][j];
                }
            }
        }
        turn += 1;
        recompute_result(A);
    }

    int imbalance() const {
        int mn = INT_MAX, mx = INT_MIN;
        for (int j = 0; j < N; j++) {
            mn = min(mn, upgCount[j]);
            mx = max(mx, upgCount[j]);
        }
        return mx - mn;
    }

    int min_upg() const {
        int mn = INT_MAX;
        for (int j = 0; j < N; j++) mn = min(mn, upgCount[j]);
        return mn;
    }

    long long approx_log2_result() const {
        // result は常に >=1 の想定（初期K=1、増加/減少しても負にはしない）
        // boost::multiprecision::msb(x) は floor(log2(x))
        return (long long)boost::multiprecision::msb(result);
    }

    double eval_key() const {
        // 評価値：log2(result) を軸に、ID強化回数の偏りをペナルティ
        return (double)approx_log2_result() - ALPHA * (double)imbalance();
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int inN, inL, inT;
    long long inK;
    cin >> inN >> inL >> inT >> inK; // 固定値だが入力形式に合わせて読む

    array<long long, N> A{};
    for (int j = 0; j < N; j++) cin >> A[j];

    array<array<long long, N>, L> C{};
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < N; j++) cin >> C[i][j];
    }

    State init;
    init.turn = 0;
    init.apples = cpp_int(K);
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < N; j++) {
            init.cnt[i][j] = 1;
            init.pw[i][j]  = 0;
        }
    }
    init.upgCount.fill(0);
    init.recompute_result(A);

    const size_t K_BEAM = 10000;
    vector<vector<State>> buckets(T + 1);
    buckets[0].push_back(std::move(init));

    auto start = chrono::steady_clock::now();
    const double TIME_LIMIT_SEC = 1.8;

    auto elapsed = [&]() -> double {
        using namespace chrono;
        return duration<double>(steady_clock::now() - start).count();
    };

    while (true) {
        bool progressed = false;

        for (int turn = 0; turn < T; turn++) {
            if (buckets[turn].empty()) break;

            // Python同様：各深さで先頭1状態のみ展開
            const State& cur = buckets[turn][0];

            // ★追加：均一化のための “緩い” フィルタ基準
            int minUpg = cur.min_upg();

            for (int machine_id = -1; machine_id < N; machine_id++) {
                for (int level = -1; level < L; level++) {
                    if ((machine_id == -1) ^ (level == -1)) continue;

                    // -1,-1 は常に許可
                    if (!(machine_id == -1 && level == -1)) {
                        // ★追加：極端に偏ったIDへの強化を抑制（概ね均一化）
                        if (cur.upgCount[machine_id] > minUpg + GAP) continue;
                    }

                    if (!cur.can_enpower(machine_id, level, C)) continue;

                    State nxt = cur;
                    if (!nxt.enpower(machine_id, level, C, A)) continue;
                    nxt.step(A);

                    buckets[turn + 1].push_back(std::move(nxt));
                    progressed = true;
                }
            }

            auto& v = buckets[turn + 1];
            if (!v.empty()) {
                // ★変更：ソート基準を eval_key()（均一化ペナルティ込み）に
                auto cmp = [](const State& a, const State& b) {
                    double ea = a.eval_key();
                    double eb = b.eval_key();
                    if (ea != eb) return ea > eb;

                    // tie-breaker: result を優先
                    if (a.result != b.result) return a.result > b.result;

                    // further tie-breaker: imbalance が小さい方
                    return a.imbalance() < b.imbalance();
                };

                if (v.size() > K_BEAM) {
                    nth_element(v.begin(), v.begin() + K_BEAM, v.end(), cmp);
                    v.resize(K_BEAM);
                }
                sort(v.begin(), v.end(), cmp);
            }

            if (elapsed() > TIME_LIMIT_SEC) goto SEARCH_END;
        }

        if (!progressed) break;
        if (elapsed() > TIME_LIMIT_SEC) break;
    }

SEARCH_END:
    int depth = T;
    while (depth > 0 && buckets[depth].empty()) depth--;

    if (buckets[depth].empty()) {
        for (int t = 0; t < T; t++) cout << -1 << "\n";
        return 0;
    }

    // 念のため最終バケットも eval_key 基準でソート
    auto& finalBucket = buckets[depth];
    auto cmp = [](const State& a, const State& b) {
        double ea = a.eval_key();
        double eb = b.eval_key();
        if (ea != eb) return ea > eb;
        if (a.result != b.result) return a.result > b.result;
        return a.imbalance() < b.imbalance();
    };
    sort(finalBucket.begin(), finalBucket.end(), cmp);

    const State& best = finalBucket[0];
    vector<pair<int,int>> ans = best.actions;

    if ((int)ans.size() < T) ans.resize(T, {-1, -1});
    if ((int)ans.size() > T) ans.resize(T);

    for (int t = 0; t < T; t++) {
        auto [lv, id] = ans[t];
        if (lv == -1 && id == -1) cout << -1 << "\n";
        else cout << lv << " " << id << "\n";
    }

    return 0;
}
