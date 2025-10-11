// g++ -O2 -std=gnu++17 -Wall -Wextra -Wshadow -o Main Main.cpp
#include <bits/stdc++.h>
using namespace std;

struct BitBoard {
    int N;
    vector<uint8_t> board; // 長さ N*N。1=セット（木 or 確認済み）、0=未セット
    BitBoard() {}
    BitBoard(int n): N(n), board(n*n, 0) {}
    BitBoard(int n, const vector<uint8_t>& b): N(n), board(b) {}

    inline int idx(int x, int y) const { return x * N + y; }

    inline void set(int x, int y) { board[idx(x,y)] = 1; }
    inline void unset(int x, int y) { board[idx(x,y)] = 0; }
    inline bool is_set(int x, int y) const { return board[idx(x,y)] != 0; }
};

static const int INF = 1e9;

// (x, y) に木を追加して良いか判定
bool is_valid(int x, int y,
              pair<int,int> current_coord,
              pair<int,int> goal,
              const BitBoard& grid_BB, // 木が1
              const BitBoard& tentative_BB) // 確認済みが1
{
    int N = grid_BB.N;
    // 範囲外
    if (x < 0 || x >= N || y < 0 || y >= N) return false;
    // 既に木
    if (grid_BB.is_set(x, y)) return false;
    // ゴールそのものは置かない
    if (make_pair(x, y) == goal) return false;
    // 確認済みマスには置かない
    if (tentative_BB.is_set(x, y)) return false;

    // (x, y) を木にしたとして、現在地からゴールへ通れるかBFSで確認
    queue<pair<int,int>> q;
    BitBoard vis(N);
    q.push(current_coord);
    vis.set(current_coord.first, current_coord.second);
    static const int dx[4] = {-1, 1, 0, 0};
    static const int dy[4] = {0, 0, -1, 1};

    while(!q.empty()){
        auto [cx, cy] = q.front(); q.pop();
        if (make_pair(cx, cy) == goal) return true;
        for(int dir=0; dir<4; dir++){
            int nx = cx + dx[dir], ny = cy + dy[dir];
            if (0 <= nx && nx < N && 0 <= ny && ny < N){
                if (!vis.is_set(nx, ny)){
                    if (!grid_BB.is_set(nx, ny) && !(nx==x && ny==y)){
                        vis.set(nx, ny);
                        q.emplace(nx, ny);
                    }
                }
            }
        }
    }
    return false; // 到達不能
}

int shortest_path_length(pair<int,int> start,
                         pair<int,int> goal,
                         const BitBoard& grid_BB)
{
    if (start == goal) return 0;
    int N = grid_BB.N;
    queue<pair<int,int>> q;
    BitBoard vis(N);
    q.push(start);
    vis.set(start.first, start.second);
    static const int dx[4] = {-1, 1, 0, 0};
    static const int dy[4] = {0, 0, -1, 1};

    int dist = 0;
    while(!q.empty()){
        dist++;
        int qs = (int)q.size();
        while(qs--){
            auto [cx, cy] = q.front(); q.pop();
            for(int dir=0; dir<4; dir++){
                int nx = cx + dx[dir], ny = cy + dy[dir];
                if (0 <= nx && nx < N && 0 <= ny && ny < N){
                    if (!grid_BB.is_set(nx, ny) && !vis.is_set(nx, ny)){
                        if (make_pair(nx, ny) == goal) return dist;
                        vis.set(nx, ny);
                        q.emplace(nx, ny);
                    }
                }
            }
        }
    }
    return INF;
}

vector<pair<int,int>> get_neighbor_05(pair<int,int> goal){
    int tx = goal.first, ty = goal.second;
    // Python版と同順序: (0,-1),(0,1),(-1,0),(1,0) × dist=1..2
    const vector<pair<int,int>> dirs = {{0,-1},{0,1},{-1,0},{1,0}};
    vector<pair<int,int>> cells;
    for(auto [dx,dy]: dirs){
        for(int d=1; d<3; d++){
            int nx = tx + dx*d, ny = ty + dy*d;
            cells.emplace_back(nx, ny);
        }
    }
    return cells;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 乱数はPython版に合わせる
    mt19937 rng(1317);

    // 時間計測
    const double TIME_LIMIT = 1.8; // 秒
    auto clock_start = chrono::high_resolution_clock::now();

    int N, tx, ty;
    if(!(cin >> N >> tx >> ty)) return 0;
    pair<int,int> goal = {tx, ty};

    vector<string> grid(N);
    for (int i=0;i<N;i++) cin >> grid[i];

    pair<int,int> current_coord = {0, N/2};

    BitBoard grid_BB(N); // 木が1
    for(int i=0;i<N;i++){
        for(int j=0;j<N;j++){
            if (grid[i][j] == 'T') grid_BB.set(i,j);
        }
    }

    BitBoard tentative_BB(N); // 確認済みが1
    tentative_BB.set(current_coord.first, current_coord.second);

    // 空きマス一覧（初期木でない場所）
    vector<pair<int,int>> empty_cells;
    empty_cells.reserve(N*N);
    for(int i=0;i<N;i++){
        for(int j=0;j<N;j++){
            if (!grid_BB.is_set(i,j)) empty_cells.emplace_back(i,j);
        }
    }

    // 追加予定座標（出力都合で一次元フラット化）
    vector<int> default_add_list;

    // 花の近囲い（候補）
    auto neighbor_cells = get_neighbor_05(goal);
    for (auto [x,y]: neighbor_cells){
        if (is_valid(x, y, current_coord, goal, grid_BB, tentative_BB)){
            grid_BB.set(x,y);
            // Python版では empty_cells.remove しているが、以後 is_valid が false を返すので省略可
            default_add_list.push_back(x);
            default_add_list.push_back(y);
        }
    }

    int max_score = -1;
    vector<int> best_add_list = default_add_list;
    BitBoard max_grid_BB(N, grid_BB.board);

    int count_trials = 0;

    // 時間までランダム試行
    for(;;){
        count_trials++;
        // シャッフル
        shuffle(empty_cells.begin(), empty_cells.end(), rng);

        vector<int> add_list = default_add_list;
        BitBoard tmp_grid_BB(N, grid_BB.board);

        // 先頭100個を順に検討（Python版と同じ）
        int upto = min<int>(100, (int)empty_cells.size());
        for(int i=0;i<upto;i++){
            auto [x,y] = empty_cells[i];
            if (is_valid(x, y, current_coord, goal, tmp_grid_BB, tentative_BB)){
                add_list.push_back(x);
                add_list.push_back(y);
                tmp_grid_BB.set(x,y);
            }
        }

        int initial_path_length = shortest_path_length(current_coord, goal, tmp_grid_BB);

        if (max_score < initial_path_length){
            max_score = initial_path_length;
            best_add_list = add_list;
            max_grid_BB = BitBoard(N, tmp_grid_BB.board);
            // cerr << "New best score: " << max_score << "\n";
        }

        auto now = chrono::high_resolution_clock::now();
        double elapsed = chrono::duration<double>(now - clock_start).count();
        if (elapsed > TIME_LIMIT) break;
    }

    vector<int> add_list = best_add_list;
    grid_BB = max_grid_BB;

    // cerr << "試行回数: " << count_trials << "\n";

    // --- インタラクティブ部（ローカルツール仕様に準拠） ---

    // 1ターン目: 現在位置
    int pi, pj;
    if(!(cin >> pi >> pj)) return 0;
    // 1ターン目: 新規確認マス
    int n;
    cin >> n;
    for(int k=0;k<n;k++){
        int x, y; cin >> x >> y;
        tentative_BB.set(x,y);
    }

    // (制約上、1ターン目でゴールには到達しないはず)
    // 木の配置を出力
    cout << (int)(add_list.size()/2);
    for(size_t i=0;i<add_list.size(); i++){
        cout << ' ' << add_list[i];
    }
    cout << '\n' << flush;
    current_coord = {pi, pj};

    // 以降のターン
    while(true){
        if(!(cin >> pi >> pj)) return 0;
        cin >> n;
        for(int k=0;k<n;k++){
            int x, y; cin >> x >> y;
            tentative_BB.set(x,y);
        }
        if (make_pair(pi,pj) == goal) break;
        cout << 0 << '\n' << flush;
        current_coord = {pi, pj};
    }
    return 0;
}
