#include <bits/stdc++.h>
#include <boost/multiprecision/cpp_int.hpp>

using namespace std;
using boost::multiprecision::cpp_int;

static constexpr int N = 10;   // fixed
static constexpr int L = 4;    // fixed
static constexpr int T = 500;  // fixed
static constexpr long long K = 1;

struct State {
    int turn = 0;
    cpp_int apples = 0;

    // machine counts can explode -> cpp_int
    array<array<cpp_int, N>, L> cnt{};
    // powers stay relatively small -> int
    array<array<int, N>, L> pw{};

    cpp_int result = 0; // predicted apples at the end if no more upgrades
    vector<pair<int,int>> actions; // (level, id) or (-1,-1)

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
            // Level 0: produce apples
            for (int j = 0; j < N; j++) {
                if (pw[0][j] != 0) {
                    apples += cpp_int(A[j]) * cnt[0][j] * pw[0][j];
                }
            }
            // Level 1..: increase lower-level machine count
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
        // invalid combos should be checked by caller
        long long base = C[level][machine_id];
        long long mul = (long long)pw[level][machine_id] + 1;
        cpp_int cost = cpp_int(base) * mul;
        return apples >= cost;
    }

    bool enpower(int machine_id, int level,
                const array<array<long long, N>, L>& C,
                const array<long long, N>& A) {
        if (machine_id == -1 && level == -1) {
            actions.push_back({-1, -1});
            return true;
        }
        long long base = C[level][machine_id];
        long long mul = (long long)pw[level][machine_id] + 1;
        cpp_int cost = cpp_int(base) * mul;

        if (apples >= cost) {
            apples -= cost;
            pw[level][machine_id] += 1;
            actions.push_back({level, machine_id});
            // NOTE: Python版はここで result 更新していたが、turn は据え置き。
            // ここでは更新してもよいが、最終的には step 後に再計算するのでどちらでも成立。
            // recompute_result(A);
            return true;
        }
        return false;
    }

    void step(const array<long long, N>& A) {
        // Level 0: produce apples
        for (int j = 0; j < N; j++) {
            if (pw[0][j] != 0) {
                apples += cpp_int(A[j]) * cnt[0][j] * pw[0][j];
            }
        }
        // Level 1..: increase lower-level machine count
        for (int i = 1; i < L; i++) {
            for (int j = 0; j < N; j++) {
                if (pw[i][j] != 0) {
                    cnt[i - 1][j] += cnt[i][j] * pw[i][j];
                }
            }
        }
        turn += 1;
        // IMPORTANT FIX:
        // Python版は step 後に result を更新していないため、深さ turn+1 の比較がズレる。
        // ここで更新する。
        recompute_result(A);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int inN, inL, inT;
    long long inK;
    cin >> inN >> inL >> inT >> inK; // ignore (they are fixed in the problem)
    array<long long, N> A{};
    for (int j = 0; j < N; j++) cin >> A[j];

    array<array<long long, N>, L> C{};
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < N; j++) cin >> C[i][j];
    }

    // Initial state
    State init;
    init.turn = 0;
    init.apples = cpp_int(K);
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < N; j++) {
            init.cnt[i][j] = 1;
            init.pw[i][j] = 0;
        }
    }
    init.recompute_result(A);

    // chokudai list: only keep best k per depth
    const size_t K_BEAM = 10000;

    vector<vector<State>> buckets(T + 1);
    buckets[0].push_back(std::move(init));

    auto start = chrono::steady_clock::now();
    const double TIME_LIMIT_SEC = 1.8;

    auto elapsed = [&]() -> double {
        using namespace chrono;
        return duration<double>(steady_clock::now() - start).count();
    };

    int maxDepth = 0;

    // Similar to the Python "while True" outer loop:
    // repeatedly expand from depth 0.. until time limit.
    while (true) {
        bool progressed = false;

        for (int turn = 0; turn < T; turn++) {
            if (buckets[turn].empty()) break;

            // Python版: chokudai_list[turn][0] を取る（先頭1個のみ展開）
            const State& cur = buckets[turn][0];

            // Expand all actions (including -1 -1)
            for (int machine_id = -1; machine_id < N; machine_id++) {
                for (int level = -1; level < L; level++) {
                    // skip (-1, x) or (x, -1)
                    if ( (machine_id == -1) ^ (level == -1) ) continue;

                    if (!cur.can_enpower(machine_id, level, C)) continue;

                    State nxt = cur; // copy (includes action history)
                    bool ok = nxt.enpower(machine_id, level, C, A);
                    if (!ok) continue; // safety
                    nxt.step(A);        // advances turn and recomputes result

                    buckets[turn + 1].push_back(std::move(nxt));
                    progressed = true;
                }
            }

            // Keep only top K_BEAM by result
            auto& v = buckets[turn + 1];
            if (!v.empty()) {
                if (v.size() > K_BEAM) {
                    nth_element(v.begin(), v.begin() + K_BEAM, v.end(),
                        [](const State& a, const State& b){ return a.result > b.result; });
                    v.resize(K_BEAM);
                }
                sort(v.begin(), v.end(),
                    [](const State& a, const State& b){ return a.result > b.result; });
                maxDepth = max(maxDepth, turn + 1);
            }

            if (elapsed() > TIME_LIMIT_SEC) {
                goto SEARCH_END;
            }
        }

        if (!progressed) break;
        if (elapsed() > TIME_LIMIT_SEC) break;
    }

SEARCH_END:
    // Choose best available depth: prefer T, else deepest reached
    int depth = T;
    while (depth > 0 && buckets[depth].empty()) depth--;
    if (buckets[depth].empty()) {
        // fallback: output all -1
        for (int t = 0; t < T; t++) cout << -1 << "\n";
        return 0;
    }

    // Ensure bucket[depth] is sorted (it should be, but just in case)
    auto& finalBucket = buckets[depth];
    sort(finalBucket.begin(), finalBucket.end(),
         [](const State& a, const State& b){ return a.result > b.result; });

    const State& best = finalBucket[0];
    vector<pair<int,int>> ans = best.actions;

    // IMPORTANT FIX: always output exactly T lines
    if ((int)ans.size() < T) {
        ans.resize(T, {-1, -1});
    } else if ((int)ans.size() > T) {
        ans.resize(T);
    }

    for (int t = 0; t < T; t++) {
        auto [lv, id] = ans[t];
        if (lv == -1 && id == -1) {
            cout << -1 << "\n";
        } else {
            cout << lv << " " << id << "\n";
        }
    }

    return 0;
}
