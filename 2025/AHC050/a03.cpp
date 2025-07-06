//  A - Gamble on Ice
//  Python 版をほぼそのまま C++ に移植
//  g++ -std=c++17 -O2 -pipe -static -s main.cpp

#include <bits/stdc++.h>
using namespace std;

using Grid     = vector<vector<int>>;
using ProbGrid = vector<vector<double>>;
const double TIME_LIMIT = 1.9;          // 探索の打ち切り秒数
const int DIRS[4][2] = {{-1,0},{1,0},{0,-1},{0,1}};

// ──────────────────────────── 盤面読み込み ────────────────────────────
Grid init_grid(int N) {
    Grid grid(N + 2, vector<int>(N + 2, 1));        // 周囲を番兵 1 で埋める
    for (int i = 1; i <= N; ++i) {
        string row;  cin >> row;
        for (int j = 1; j <= N; ++j)
            if (row[j - 1] == '.') grid[i][j] = 0;
    }
    return grid;
}

// ───────────────────── 空マス一覧（1-indexed） ──────────────────────
vector<pair<int,int>> empty_cells(const Grid& grid, int N) {
    vector<pair<int,int>> cells;
    for (int i = 1; i <= N; ++i)
        for (int j = 1; j <= N; ++j)
            if (!grid[i][j]) cells.emplace_back(i, j);
    return cells;
}

// ─────────────────────── 確率グリッド初期化 ────────────────────────
ProbGrid init_prob_grid(const Grid& grid, int N, int M) {
    ProbGrid prob(N + 2, vector<double>(N + 2, 0.0));
    double p = 1.0 / double(N * N - M);
    for (int i = 1; i <= N; ++i)
        for (int j = 1; j <= N; ++j)
            if (!grid[i][j]) prob[i][j] = p;
    return prob;
}

// ─────────────────────── 確率グリッド更新 ──────────────────────────
ProbGrid calc_prob(const Grid& grid, const ProbGrid& prob_grid, int N) {
    vector<pair<int,int>> coord_list;                                // index → 座標
    vector<vector<array<int,4>>> dst(N + 2, vector<array<int,4>>(N + 2));
    int idx = 0;

    // 上方向
    for (int j = 1; j <= N; ++j)
        for (int i = N; i >= 1; --i)
            if (!grid[i][j]) {
                dst[i][j][0] = idx;
                if (grid[i - 1][j]) { coord_list.emplace_back(i, j); ++idx; }
            }
    // 下方向
    for (int j = 1; j <= N; ++j)
        for (int i = 1; i <= N; ++i)
            if (!grid[i][j]) {
                dst[i][j][1] = idx;
                if (grid[i + 1][j]) { coord_list.emplace_back(i, j); ++idx; }
            }
    // 左方向
    for (int i = 1; i <= N; ++i)
        for (int j = N; j >= 1; --j)
            if (!grid[i][j]) {
                dst[i][j][2] = idx;
                if (grid[i][j - 1]) { coord_list.emplace_back(i, j); ++idx; }
            }
    // 右方向
    for (int i = 1; i <= N; ++i)
        for (int j = 1; j <= N; ++j)
            if (!grid[i][j]) {
                dst[i][j][3] = idx;
                if (grid[i][j + 1]) { coord_list.emplace_back(i, j); ++idx; }
            }

    ProbGrid next(N + 2, vector<double>(N + 2, 0.0));
    for (int i = 1; i <= N; ++i)
        for (int j = 1; j <= N; ++j) {
            if (grid[i][j]) { next[i][j] = 9.9; continue; }
            double q = prob_grid[i][j] * 0.25;
            for (int d = 0; d < 4; ++d) {
                auto [x, y] = coord_list[ dst[i][j][d] ];
                next[x][y] += q;
            }
        }
    return next;
}

// ─────────────────────────── 状態構造体 ────────────────────────────
struct State {
    bool not_visited;
    double money, live_prob;
    Grid grid;
    vector<pair<int,int>> cells;
    ProbGrid prob_grid;
    pair<int,int> coord;  // 出力用（0-indexed）
    int prev;
};

// ───────────────────────────── 探索本体 ────────────────────────────
vector<pair<int,int>> solve(Grid grid, int N, int M) {
    int remaining = N*N - M;
    auto cells = empty_cells(grid, N);
    auto prob  = init_prob_grid(grid, N, M);

    vector<vector<int>> chokudai(remaining + 1);
    vector<State> states;  states.reserve(100000);

    states.push_back({true, 0.0, 1.0, grid, cells, prob, {-1,-1}, -1});
    chokudai[0].push_back(0);

    auto t0 = chrono::steady_clock::now();
    auto elapsed = [&]{ return chrono::duration<double>(chrono::steady_clock::now() - t0).count(); };

    while (elapsed() < TIME_LIMIT) {
        for (size_t depth = 0; depth < chokudai.size(); ++depth) {
            if (chokudai[depth].empty()) continue;
            int cur_id = chokudai[depth][0];
            auto &cur = states[cur_id];
            if (!cur.not_visited) continue;
            cur.not_visited = false;

            auto prob2 = calc_prob(cur.grid, cur.prob_grid, N);

            // 生存確率の低い（=安全な）1/10 を候補に
            sort(cur.cells.begin(), cur.cells.end(),
                 [&](auto &a, auto &b){ return prob2[a.first][a.second] > prob2[b.first][b.second]; });
            size_t start = cur.cells.size() - (cur.cells.size() / 100 + 1);  // 1/100に変更

            for (size_t k = start; k < cur.cells.size(); ++k) {
                auto [x, y] = cur.cells[k];

                Grid   nxt_grid = cur.grid;   nxt_grid[x][y] = 1;
                double nxt_live = cur.live_prob - prob2[x][y];
                double nxt_money = cur.money + cur.live_prob;

                vector<pair<int,int>> nxt_cells;
                nxt_cells.reserve(cur.cells.size() - 1);
                for (auto &c : cur.cells) if (c != make_pair(x,y)) nxt_cells.push_back(c);

                states.push_back({true, nxt_money, nxt_live, move(nxt_grid),
                                  move(nxt_cells), prob2, {x-1, y-1}, cur_id});
                int nxt_id = (int)states.size() - 1;
                if (depth + 1 < chokudai.size()) chokudai[depth + 1].push_back(nxt_id);
            }
            if (depth != remaining && !chokudai[depth + 1].empty()) {
                auto cmp = [&](int a, int b) {
                    auto &s1 = states[a]; auto &s2 = states[b];
                    if (s1.not_visited != s2.not_visited) return s1.not_visited > s2.not_visited;
                    if (s1.money != s2.money)             return s1.money      > s2.money;
                    return s1.live_prob > s2.live_prob;
                };
                sort(chokudai[depth + 1].begin(), chokudai[depth + 1].end(), cmp);
            }
        }
    }

    if (chokudai.back().empty()) return {};
    sort(chokudai.back().begin(), chokudai.back().end(),
         [&](int a, int b){ return states[a].money > states[b].money; });
    int best = chokudai.back()[0];

    vector<pair<int,int>> ans;
    for (int id = best; id != -1; id = states[id].prev)
        if (states[id].coord.first != -1) ans.push_back(states[id].coord);
    reverse(ans.begin(), ans.end());
    return ans;
}

// ─────────────────────────────── main ───────────────────────────────
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M;  if (!(cin >> N >> M)) return 0;
    auto grid = init_grid(N);
    auto ans  = solve(grid, N, M);

    int need = N*N - M;
    for (int i = 0; i < need && i < (int)ans.size(); ++i)
        cout << ans[i].first << ' ' << ans[i].second << '\n';
    for (int i = (int)ans.size(); i < need; ++i)   // 不足分は (0,0) で埋める
        cout << "0 0\n";
    return 0;
}
