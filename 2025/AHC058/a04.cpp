#include <bits/stdc++.h>
using namespace std;

static constexpr int N = 10;
static constexpr int L = 4;
static constexpr int T = 500;

using u64  = uint64_t;
using u128 = __uint128_t;

static constexpr u64 CAP = std::numeric_limits<u64>::max(); // saturate to u64 max

static inline u64 sat_add(u64 a, u64 b) {
    u128 s = (u128)a + (u128)b;
    return (s > (u128)CAP) ? CAP : (u64)s;
}
static inline u64 sat_sub(u64 a, u64 b) { // caller must ensure a>=b; if not, clamp to 0
    return (a >= b) ? (a - b) : 0;
}
static inline u64 sat_mul(u64 a, u64 b) {
    u128 p = (u128)a * (u128)b;
    return (p > (u128)CAP) ? CAP : (u64)p;
}

// nC2, nC3, nC4 for n up to 500 (fits in u64)
static inline u64 comb2(u64 n) { return (n >= 2) ? (n * (n - 1) / 2) : 0; }
static inline u64 comb3(u64 n) { return (n >= 3) ? (n * (n - 1) * (n - 2) / 6) : 0; }
static inline u64 comb4(u64 n) { return (n >= 4) ? (n * (n - 1) * (n - 2) * (n - 3) / 24) : 0; }

struct Node {
    int turn = 0;
    u64 apples = 0;

    // counts, powers
    u64 cnt[L][N];
    uint16_t pw[L][N];

    // parent reconstruction
    int parent = -1;        // index in pool
    int16_t act_level = -2; // action taken to reach this node
    int16_t act_id    = -2;

    // evaluation key: predicted apples at end if no more upgrades (lower bound, saturated)
    u64 score = 0;
};

// O(N) closed-form prediction for "no more upgrades" from current state
static inline u64 predict_no_upgrade_score(const Node& s, const array<u64, N>& A) {
    int r_i = T - s.turn;
    if (r_i <= 0) return s.apples;
    u64 r = (u64)r_i;

    u64 C2 = comb2(r);
    u64 C3 = comb3(r);
    u64 C4 = comb4(r);

    u64 total = s.apples;

    for (int j = 0; j < N; j++) {
        u64 b0 = s.cnt[0][j];
        u64 b1 = s.cnt[1][j];
        u64 b2 = s.cnt[2][j];
        u64 b3 = s.cnt[3][j];

        u64 p0 = (u64)s.pw[0][j];
        u64 p1 = (u64)s.pw[1][j];
        u64 p2 = (u64)s.pw[2][j];
        u64 p3 = (u64)s.pw[3][j];

        if (p0 == 0) continue; // no production without p0

        // Sum_{t=0..r-1} b0(t) =
        //   r*b0
        // + C(r,2)*b1*p1
        // + C(r,3)*b2*p2*p1
        // + C(r,4)*b3*p3*p2*p1
        u64 term0 = sat_mul(b0, r);

        u64 term1 = 0;
        if (C2 && b1 && p1) term1 = sat_mul(C2, sat_mul(b1, p1));

        u64 term2 = 0;
        if (C3 && b2 && p2 && p1) term2 = sat_mul(C3, sat_mul(sat_mul(b2, p2), p1));

        u64 term3 = 0;
        if (C4 && b3 && p3 && p2 && p1) term3 = sat_mul(C4, sat_mul(sat_mul(sat_mul(b3, p3), p2), p1));

        u64 sumB0 = sat_add(term0, sat_add(term1, sat_add(term2, term3)));

        // gain = A[j] * p0 * sumB0
        u64 base = sat_mul(A[j], p0);     // A<=100, p0<=~500
        u64 gain = sat_mul(base, sumB0);

        total = sat_add(total, gain);
    }

    return total;
}

// one turn step: (after optional upgrade) produce then cascade counts
static inline void step_one_turn(Node& s, const array<u64, N>& A) {
    // Level 0 produce
    for (int j = 0; j < N; j++) {
        u64 p0 = (u64)s.pw[0][j];
        if (!p0) continue;
        u64 base = sat_mul(A[j], p0);          // small
        u64 add  = sat_mul(s.cnt[0][j], base); // cnt0 * (A*p0)
        s.apples = sat_add(s.apples, add);
    }
    // Level 1..3 cascade counts downward
    for (int i = 1; i < L; i++) {
        for (int j = 0; j < N; j++) {
            u64 p = (u64)s.pw[i][j];
            if (!p) continue;
            u64 inc = sat_mul(s.cnt[i][j], p);
            s.cnt[i - 1][j] = sat_add(s.cnt[i - 1][j], inc);
        }
    }
    s.turn++;
}

static inline bool try_upgrade(Node& s, int level, int id,
                               const array<array<u64, N>, L>& C) {
    if (level == -1 && id == -1) return true;

    // cost = C[level][id] * (pw+1)
    u64 pw = (u64)s.pw[level][id];
    u128 cost128 = (u128)C[level][id] * (u128)(pw + 1);
    u64 cost = (cost128 > (u128)CAP) ? CAP : (u64)cost128;

    if (s.apples < cost) return false; // conservative (safe)
    s.apples = sat_sub(s.apples, cost);
    s.pw[level][id] = (uint16_t)(s.pw[level][id] + 1);
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int inN, inL, inT;
    long long inK;
    cin >> inN >> inL >> inT >> inK;

    array<u64, N> A{};
    for (int j = 0; j < N; j++) cin >> A[j];

    array<array<u64, N>, L> C{};
    for (int i = 0; i < L; i++) {
        for (int j = 0; j < N; j++) cin >> C[i][j];
    }

    // Prebuild action list: (-1,-1) + all (level,id)
    vector<pair<int,int>> actions;
    actions.reserve(1 + L * N);
    actions.push_back({-1, -1});
    for (int i = 0; i < L; i++) for (int j = 0; j < N; j++) actions.push_back({i, j});

    // Parameters
    const int K_BEAM = 5000;            // smaller => faster
    const int PRUNE_TH = K_BEAM * 2;    // prune when exceeds
    const double TIME_LIMIT = 1.80;     // seconds (match typical heuristic TL)

    auto start = chrono::steady_clock::now();
    auto elapsed = [&]() -> double {
        return chrono::duration<double>(chrono::steady_clock::now() - start).count();
    };

    // Pool storage + buckets as indices
    vector<Node> pool;
    pool.reserve(200000);

    vector<vector<int>> bucket(T + 1);
    vector<int> ptr(T + 1, 0);

    auto cmp_idx = [&](int a, int b) {
        return pool[a].score > pool[b].score;
    };

    auto normalize_bucket = [&](int d) {
        auto& v = bucket[d];

        // drop expanded prefix by compaction when pointer grows
        if (ptr[d] > 0 && (ptr[d] > K_BEAM || (int)v.size() > PRUNE_TH)) {
            vector<int> nv;
            nv.reserve(max(0, (int)v.size() - ptr[d]));
            for (int i = ptr[d]; i < (int)v.size(); i++) nv.push_back(v[i]);
            v.swap(nv);
            ptr[d] = 0;
        }

        if ((int)v.size() > PRUNE_TH) {
            // keep top K_BEAM
            nth_element(v.begin(), v.begin() + K_BEAM, v.end(), cmp_idx);
            v.resize(K_BEAM);
            sort(v.begin(), v.end(), cmp_idx);
        } else {
            // keep it sorted if it is small-ish
            sort(v.begin(), v.end(), cmp_idx);
            if ((int)v.size() > K_BEAM) v.resize(K_BEAM);
        }
    };

    // initial node
    Node root;
    root.turn = 0;
    root.apples = 1; // K=1 fixed by problem
    for (int i = 0; i < L; i++) for (int j = 0; j < N; j++) {
        root.cnt[i][j] = 1;
        root.pw[i][j] = 0;
    }
    root.parent = -1;
    root.act_level = -2;
    root.act_id = -2;
    root.score = predict_no_upgrade_score(root, A);

    pool.push_back(root);
    bucket[0].push_back(0);
    normalize_bucket(0);

    // Proper chokudai: iterate, each depth expands one "next best unexpanded" state
    while (elapsed() < TIME_LIMIT) {
        bool progressed = false;

        for (int d = 0; d < T; d++) {
            if (elapsed() >= TIME_LIMIT) break;
            normalize_bucket(d);
            if (ptr[d] >= (int)bucket[d].size()) continue;

            int cur_idx = bucket[d][ptr[d]++];
            // IMPORTANT: Do not keep a reference into `pool` here.
            // `pool.push_back()` below may reallocate and invalidate references.
            const Node cur = pool[cur_idx];

            // Expand all actions
            for (auto [lv, id] : actions) {
                if (elapsed() >= TIME_LIMIT) break;

                Node nxt = cur;
                nxt.parent = cur_idx;
                nxt.act_level = (int16_t)lv;
                nxt.act_id    = (int16_t)id;

                if (!try_upgrade(nxt, lv, id, C)) continue;
                step_one_turn(nxt, A);
                nxt.score = predict_no_upgrade_score(nxt, A);

                int nxt_idx = (int)pool.size();
                pool.push_back(nxt);
                bucket[d + 1].push_back(nxt_idx);
            }

            normalize_bucket(d + 1);
            progressed = true;
        }

        if (!progressed) break;
    }

    // Choose best available depth (prefer T, else deepest non-empty)
    int best_depth = T;
    while (best_depth > 0 && bucket[best_depth].empty()) best_depth--;
    if (bucket[best_depth].empty()) {
        for (int t = 0; t < T; t++) cout << -1 << "\n";
        return 0;
    }
    normalize_bucket(best_depth);

    int best_idx = bucket[best_depth][0];

    // Reconstruct actions by parent pointers
    vector<pair<int,int>> ans;
    ans.reserve(T);

    int cur = best_idx;
    while (cur != -1 && pool[cur].parent != -1) {
        ans.push_back({pool[cur].act_level, pool[cur].act_id});
        cur = pool[cur].parent;
    }
    reverse(ans.begin(), ans.end());

    // Output exactly T lines
    if ((int)ans.size() < T) ans.resize(T, {-1, -1});
    else if ((int)ans.size() > T) ans.resize(T);

    for (int t = 0; t < T; t++) {
        auto [lv, id] = ans[t];
        if (lv == -1 && id == -1) cout << -1 << "\n";
        else cout << lv << " " << id << "\n";
    }

    return 0;
}
