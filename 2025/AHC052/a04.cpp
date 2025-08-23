#include <bits/stdc++.h>
using namespace std;

// ====== 定数（問題では N=30, M=10, K=10 が固定ですが、入力からも読みます） ======

struct BitBoard {
    // 30x30 = 900 マスをビットで管理
    bitset<900> board;
    int visit_count;

    BitBoard() : board(), visit_count(0) {}

    // コピー用コンストラクタ
    BitBoard(const bitset<900>& b, int cnt) : board(b), visit_count(cnt) {}

    inline int idx(int x, int y) const { // x = 行(i), y = 列(j)
        return y * 30 + x;
    }

    inline bool has_visited(int x, int y) const {
        return board.test(idx(x, y));
    }

    inline void visit(int x, int y) {
        int id = idx(x, y);
        if (!board.test(id)) {
            board.set(id);
            visit_count++;
        }
    }
};

// 近傍で未訪問のマスを BFS で探す
pair<int,int> find_nearest_unvisited(
    const BitBoard& BB,
    int sx, int sy,
    const vector<vector<int>>& X_wall, // (N-1) x N : 上下（縦）を阻害
    const vector<vector<int>>& Y_wall  // N x (N-1) : 左右（横）を阻害
) {
    const int N = 30;
    queue<pair<int,int>> q;
    vector<vector<char>> vis(N, vector<char>(N, 0));
    q.push({sx, sy});
    vis[sx][sy] = 1;

    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();

        if (!BB.has_visited(x, y)) {
            return {x, y};
        }

        // 上
        if (x-1 >= 0 && !vis[x-1][y]) {
            if (X_wall[x-1][y] == 0) {
                vis[x-1][y] = 1;
                q.push({x-1, y});
            }
        }
        // 下
        if (x+1 < N && !vis[x+1][y]) {
            if (X_wall[x][y] == 0) {
                vis[x+1][y] = 1;
                q.push({x+1, y});
            }
        }
        // 左
        if (y-1 >= 0 && !vis[x][y-1]) {
            if (Y_wall[x][y-1] == 0) {
                vis[x][y-1] = 1;
                q.push({x, y-1});
            }
        }
        // 右
        if (y+1 < N && !vis[x][y+1]) {
            if (Y_wall[x][y] == 0) {
                vis[x][y+1] = 1;
                q.push({x, y+1});
            }
        }
    }
    return {-1, -1}; // 見つからなかった
}

// 目的地への最短路の「最初の一手」を BFS で求める
char get_next_step(
    int rx, int ry,
    int tx, int ty,
    const vector<vector<int>>& X_wall,
    const vector<vector<int>>& Y_wall
) {
    const int N = 30;
    if (rx == tx && ry == ty) return 'S';

    struct Node { int x, y; char first; };
    queue<Node> q;
    vector<vector<char>> vis(N, vector<char>(N, 0));

    q.push({rx, ry, 0});
    vis[rx][ry] = 1;

    while (!q.empty()) {
        Node cur = q.front(); q.pop();

        if (cur.x == tx && cur.y == ty) {
            return cur.first ? cur.first : 'S';
        }

        // 上へ
        if (cur.x - 1 >= 0 && !vis[cur.x - 1][cur.y]) {
            if (X_wall[cur.x - 1][cur.y] == 0) {
                vis[cur.x - 1][cur.y] = 1;
                char nd = cur.first ? cur.first : 'U';
                q.push({cur.x - 1, cur.y, nd});
            }
        }
        // 下へ
        if (cur.x + 1 < N && !vis[cur.x + 1][cur.y]) {
            if (X_wall[cur.x][cur.y] == 0) {
                vis[cur.x + 1][cur.y] = 1;
                char nd = cur.first ? cur.first : 'D';
                q.push({cur.x + 1, cur.y, nd});
            }
        }
        // 左へ
        if (cur.y - 1 >= 0 && !vis[cur.x][cur.y - 1]) {
            if (Y_wall[cur.x][cur.y - 1] == 0) {
                vis[cur.x][cur.y - 1] = 1;
                char nd = cur.first ? cur.first : 'L';
                q.push({cur.x, cur.y - 1, nd});
            }
        }
        // 右へ
        if (cur.y + 1 < N && !vis[cur.x][cur.y + 1]) {
            if (Y_wall[cur.x][cur.y] == 0) {
                vis[cur.x][cur.y + 1] = 1;
                char nd = cur.first ? cur.first : 'R';
                q.push({cur.x, cur.y + 1, nd});
            }
        }
    }
    return 'S';
}

// ロボット群を 1 回操作して状態を更新
void move_robot(
    BitBoard& BB,
    vector<pair<int,int>>& robots,
    const vector<vector<char>>& key_config, // K x M
    int key,
    const vector<vector<int>>& X_wall,
    const vector<vector<int>>& Y_wall
) {
    const int N = 30;
    const int M = (int)robots.size();

    for (int i = 0; i < M; ++i) {
        char d = key_config[key][i];
        int x = robots[i].first;
        int y = robots[i].second;
        int nx = x, ny = y;

        if (d == 'U') nx = x - 1;
        else if (d == 'D') nx = x + 1;
        else if (d == 'L') ny = y - 1;
        else if (d == 'R') ny = y + 1;
        else { // 'S'
            continue;
        }

        if (0 <= nx && nx < N && 0 <= ny && ny < N) {
            bool can_move = false;
            if (d == 'U' && X_wall[nx][ny] == 0) can_move = true;              // h_{nx,ny}
            else if (d == 'D' && X_wall[nx - 1][ny] == 0) can_move = true;     // h_{x, y}
            else if (d == 'L' && Y_wall[nx][ny] == 0) can_move = true;         // v_{x, y-1}（nyは既に-1済み）
            else if (d == 'R' && Y_wall[nx][ny - 1] == 0) can_move = true;     // v_{x, y}

            if (can_move) {
                robots[i] = {nx, ny};
                BB.visit(nx, ny);
            }
        }
    }
}

// ビームサーチで次状態を生成
struct State {
    BitBoard bb;
    vector<pair<int,int>> robots;
    vector<int> ans; // 押したボタン列（※原実装では後続で使っていないが移植して保持）
};

vector<State> generate_next_states(
    const BitBoard& BB,
    const vector<pair<int,int>>& robots,
    const vector<int>& ans,
    const vector<vector<char>>& key_config,
    const vector<vector<int>>& X_wall,
    const vector<vector<int>>& Y_wall
) {
    vector<State> res;
    for (int key = 0; key < 4; ++key) { // 0..3 のみ
        State st;
        st.bb = BitBoard(BB.board, BB.visit_count);
        st.robots = robots;
        st.ans = ans;

        move_robot(st.bb, st.robots, key_config, key, X_wall, Y_wall);
        st.ans.push_back(key);
        res.push_back(std::move(st));
    }
    return res;
}

// 方向文字 -> ボタン番号
int dir2key(char c) {
    switch (c) {
        case 'U': return 0;
        case 'D': return 1;
        case 'L': return 2;
        case 'R': return 3;
        default:  return 4; // 'S'
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // パラメータ読み込み
    int N_in, M_in, K_in;
    if (!(cin >> N_in >> M_in >> K_in)) return 0;
    const int N = 30, M = 10, K = 10; // ロジック上は 30/10/10 を想定

    vector<pair<int,int>> robots(M);
    for (int i = 0; i < M; ++i) {
        int a, b; cin >> a >> b;
        robots[i] = {a, b};
    }

    // Y_wall: N 行, 各行 (N-1) 文字
    vector<vector<int>> Y_wall(N, vector<int>(N-1, 0));
    for (int i = 0; i < N; ++i) {
        string s; cin >> s;
        for (int j = 0; j < N-1; ++j) Y_wall[i][j] = (s[j] - '0');
    }

    // X_wall: (N-1) 行, 各行 N 文字
    vector<vector<int>> X_wall(N-1, vector<int>(N, 0));
    for (int i = 0; i < N-1; ++i) {
        string s; cin >> s;
        for (int j = 0; j < N; ++j) X_wall[i][j] = (s[j] - '0');
    }

    // キーコンフィグ初期化
    vector<vector<char>> key_config(K, vector<char>(M, 'S'));
    // 0:U, 1:D, 2:L, 3:R を全ロボットに割り当て
    for (int m = 0; m < M; ++m) {
        key_config[0][m] = 'U';
        key_config[1][m] = 'D';
        key_config[2][m] = 'L';
        key_config[3][m] = 'R';
    }

    BitBoard BB;
    // 初期位置を訪問済みに
    for (auto &p : robots) BB.visit(p.first, p.second);

    // 以降は原実装のロジックを忠実に移植
    const int BEAM_WIDTH = 1000;
    const double TIME_LIMIT = 1.5; // 秒
    const int LEN = 500;

    vector<int> ans_list; // 出力する操作列

    // ビームサーチ（※原実装同様、結果は実状態に反映しない）
    vector<State> current_states;
    current_states.push_back(State{BB, robots, {}});

    std::mt19937_64 rng(1317);
    std::uniform_real_distribution<double> dist(0.0, 1.0);

    auto t0 = chrono::steady_clock::now();

    for (int step = 0; step < LEN; ++step) {
        auto t1 = chrono::steady_clock::now();
        double elapsed = chrono::duration<double>(t1 - t0).count();
        if (elapsed > TIME_LIMIT) break;

        vector<State> next_states;
        next_states.reserve(current_states.size() * 4);

        for (const auto& st : current_states) {
            auto tmp = generate_next_states(st.bb, st.robots, st.ans, key_config, X_wall, Y_wall);
            for (auto &ns : tmp) next_states.push_back(std::move(ns));
        }

        // 訪問マス数 + 乱数 でソートして上位だけ残す
        vector<pair<double,int>> key_idx;
        key_idx.reserve(next_states.size());
        for (int i = 0; i < (int)next_states.size(); ++i) {
            double score = next_states[i].bb.visit_count + dist(rng);
            key_idx.push_back({score, i});
        }
        sort(key_idx.begin(), key_idx.end(), [&](const auto& a, const auto& b){
            return a.first > b.first;
        });

        vector<State> trimmed;
        int keep = min(BEAM_WIDTH, (int)key_idx.size());
        trimmed.reserve(keep);
        for (int i = 0; i < keep; ++i) trimmed.push_back(std::move(next_states[key_idx[i].second]));
        current_states.swap(trimmed);
    }

    // 親機（中心 (15,15) に最も近いロボット）を選ぶ
    int main_robot_id = 0;
    {
        int best = INT_MAX;
        for (int i = 0; i < M; ++i) {
            int x = robots[i].first, y = robots[i].second;
            int dist2 = (x - 15) * (x - 15) + (y - 15) * (y - 15);
            if (dist2 < best) {
                best = dist2;
                main_robot_id = i;
            }
        }
    }

    // すべてのマスに訪れるまで（または詰まるまで）
    while (BB.visit_count < 900) {
        auto [tx, ty] = find_nearest_unvisited(BB, robots[main_robot_id].first, robots[main_robot_id].second, X_wall, Y_wall);
        char next_step = get_next_step(robots[main_robot_id].first, robots[main_robot_id].second, tx, ty, X_wall, Y_wall);
        if (next_step == 'S') break;
        int key = dir2key(next_step);
        ans_list.push_back(key);
        move_robot(BB, robots, key_config, key, X_wall, Y_wall);
    }

    // ===== 出力 =====
    // キーコンフィグ K 行（各行 M 文字をスペース区切り）
    for (int i = 0; i < K; ++i) {
        for (int j = 0; j < M; ++j) {
            if (j) cout << ' ';
            cout << key_config[i][j];
        }
        cout << '\n';
    }
    // 操作列（1 行 1 数字）
    for (int a : ans_list) cout << a << '\n';

    // 標準エラー出力にスコアを出す（デバッグ用）
    cerr << 3*N*N - ans_list.size() << endl;

    return 0;
}
