#include <bits/stdc++.h>
using namespace std;

// ====== 乱数 ======
static mt19937 rng(1317);
template<class T> inline T randint(T l, T r){ uniform_int_distribution<T> dist(l, r); return dist(rng); }

// ====== 計時 ======
struct Timer {
    chrono::steady_clock::time_point st;
    Timer(){ reset(); }
    void reset(){ st = chrono::steady_clock::now(); }
    double elapsed() const {
        using namespace chrono;
        return duration_cast<duration<double>>(steady_clock::now() - st).count();
    }
};

// ====== ビットボード (N*N <= 1600 を想定) ======
struct BitBoard {
    int N;
    vector<uint64_t> bits; // (N*N+63)/64
    BitBoard() {}
    BitBoard(int N_, uint64_t fill=0): N(N_) {
        size_t L = (N*N + 63) >> 6;
        bits.assign(L, 0ULL);
        if(fill) for(auto &b: bits) b = fill;
    }
    inline void set(int x, int y){
        int idx = x * N + y;
        bits[idx >> 6] |= (1ULL << (idx & 63));
    }
    inline void unset(int x, int y){
        int idx = x * N + y;
        bits[idx >> 6] &= ~(1ULL << (idx & 63));
    }
    inline bool is_set(int x, int y) const {
        int idx = x * N + y;
        return (bits[idx >> 6] >> (idx & 63)) & 1ULL;
    }
};

// ====== ユーティリティ ======
static const int INF = 1e9;
static const int dx4[4] = {-1, 1, 0, 0};
static const int dy4[4] = { 0, 0,-1, 1};

inline bool in_grid(int x, int y, int N){
    return 0 <= x && x < N && 0 <= y && y < N;
}

// (デバッグ用) マス状態
inline string cell_status(int x, int y, const BitBoard &grid_BB){
    if(!in_grid(x,y,grid_BB.N)) return "Not in grid";
    return grid_BB.is_set(x,y) ? "Tree" : "Empty";
}

// 最短距離
int shortest_path_length(pair<int,int> start, pair<int,int> goal, const BitBoard &grid_BB){
    if(start == goal) return 0;
    int N = grid_BB.N;
    deque<pair<int,int>> q;
    q.push_back(start);
    BitBoard vis(N);
    vis.set(start.first, start.second);
    int dist = 0;
    while(!q.empty()){
        int qs = (int)q.size();
        ++dist;
        while(qs--){
            auto [cx, cy] = q.front(); q.pop_front();
            for(int d=0; d<4; ++d){
                int nx = cx + dx4[d], ny = cy + dy4[d];
                if(in_grid(nx,ny,N) && !grid_BB.is_set(nx,ny) && !vis.is_set(nx,ny)){
                    if(make_pair(nx,ny) == goal) return dist;
                    vis.set(nx,ny);
                    q.emplace_back(nx,ny);
                }
            }
        }
    }
    return INF;
}

// 最短経路を復元
vector<pair<int,int>> get_shortest_path(pair<int,int> start, pair<int,int> goal, const BitBoard &grid_BB){
    if(start == goal) return {start};
    int N = grid_BB.N;
    deque<pair<int,int>> q;
    q.push_back(start);
    BitBoard vis(N);
    vis.set(start.first, start.second);

    vector<int> parent(N*N, -1);
    auto idx = [&](int x, int y){ return x*N + y; };

    while(!q.empty()){
        auto [cx, cy] = q.front(); q.pop_front();
        for(int d=0; d<4; ++d){
            int nx = cx + dx4[d], ny = cy + dy4[d];
            if(in_grid(nx,ny,N) && !grid_BB.is_set(nx,ny) && !vis.is_set(nx,ny)){
                vis.set(nx,ny);
                parent[idx(nx,ny)] = idx(cx,cy);
                if(make_pair(nx,ny) == goal){
                    vector<pair<int,int>> path;
                    int cur = idx(nx,ny);
                    while(cur != -1){
                        int x = cur / N, y = cur % N;
                        path.emplace_back(x,y);
                        cur = parent[cur];
                    }
                    reverse(path.begin(), path.end());
                    return path;
                }
                q.emplace_back(nx,ny);
            }
        }
    }
    return {};
}

// (x,y) に木を置いても入口->花の経路が残るか
bool is_valid(int x, int y, pair<int,int> current_coord, pair<int,int> goal, const BitBoard &grid_BB, const BitBoard &tentative_BB){
    int N = grid_BB.N;
    if(!in_grid(x,y,N)) return false;
    if(grid_BB.is_set(x,y)) return false;
    if(make_pair(x,y) == goal) return false;
    if(tentative_BB.is_set(x,y)) return false;

    // BFS で (x,y) を塞いだ上で current -> goal が可能か
    deque<pair<int,int>> q;
    q.push_back(current_coord);
    BitBoard vis(N);
    vis.set(current_coord.first, current_coord.second);
    while(!q.empty()){
        auto [cx, cy] = q.front(); q.pop_front();
        if(make_pair(cx,cy) == goal) return true;
        for(int d=0; d<4; ++d){
            int nx = cx + dx4[d], ny = cy + dy4[d];
            if(in_grid(nx,ny,N) && !vis.is_set(nx,ny)){
                if(grid_BB.is_set(nx,ny)) continue;
                if(nx == x && ny == y) continue; // ここに木を置く
                vis.set(nx,ny);
                q.emplace_back(nx,ny);
            }
        }
    }
    return false;
}

// is_vaild_11: 最短経路上でないなら許可、上なら仮置きして新経路が存在するかで判断
pair<bool, unordered_set<int>> is_valid_11(
    int x, int y,
    pair<int,int> current_coord,
    pair<int,int> goal,
    const BitBoard &grid_BB,
    const BitBoard &tentative_BB,
    const unordered_set<int> &shortest_path_set_in
){
    int N = grid_BB.N;
    auto idx = [&](int a, int b){ return a*N + b; };
    unordered_set<int> sps = shortest_path_set_in;

    if(!in_grid(x,y,N)) return {false, sps};
    if(grid_BB.is_set(x,y)) return {false, sps};
    if(make_pair(x,y) == goal) return {false, sps};
    if(tentative_BB.is_set(x,y)) return {false, sps};

    int id = idx(x,y);
    if(!sps.count(id)) return {true, sps};

    BitBoard new_grid = grid_BB;
    new_grid.set(x,y);
    auto new_path = get_shortest_path(current_coord, goal, new_grid);
    if(!new_path.empty()){
        unordered_set<int> ns;
        ns.reserve(new_path.size()*2);
        for(auto &p: new_path) ns.insert(idx(p.first, p.second));
        return {true, ns};
    }
    return {false, sps};
}

// 花の近傍: 0,±1,±2 (方向固定)
vector<pair<int,int>> get_neighbor_05(pair<int,int> goal){
    int tx = goal.first, ty = goal.second;
    vector<pair<int,int>> cells;
    // directions = (0, -1), (0, 1), (-1, 0), (1, 0) の距離1,2
    const int vx[4] = {0, 0, -1, 1};
    const int vy[4] = {-1, 1, 0, 0};
    for(int d=0; d<4; ++d){
        for(int dist=1; dist<=2; ++dist){
            cells.emplace_back(tx + vx[d]*dist, ty + vy[d]*dist);
        }
    }
    return cells;
}

// 花の近傍: 特定の6マス
vector<pair<int,int>> get_neighbor_08(pair<int,int> goal){
    int tx = goal.first, ty = goal.second;
    vector<pair<int,int>> cells;
    cells.emplace_back(tx, ty-1);
    cells.emplace_back(tx, ty+1);
    cells.emplace_back(tx-1, ty);
    cells.emplace_back(tx+2, ty);
    cells.emplace_back(tx+1, ty+1);
    cells.emplace_back(tx+1, ty-1);
    return cells;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    Timer timer;
    const double TIME_LIMIT = 1.8; // 秒（テスター用に伸ばしたい場合は変更）

    int N, tx, ty;
    if(!(cin >> N >> tx >> ty)) return 0;
    pair<int,int> goal = {tx, ty};

    vector<string> grid(N);
    for(int i=0;i<N;++i) cin >> grid[i];

    pair<int,int> current_coord = {0, N/2};

    BitBoard grid_BB(N);
    for(int i=0;i<N;++i){
        for(int j=0;j<N;++j){
            if(grid[i][j] == 'T') grid_BB.set(i,j);
        }
    }

    BitBoard tentative_BB(N);
    tentative_BB.set(current_coord.first, current_coord.second);

    // 空きマス一覧
    vector<pair<int,int>> empty_cells;
    empty_cells.reserve(N*N);
    for(int i=0;i<N;++i){
        for(int j=0;j<N;++j){
            if(!grid_BB.is_set(i,j)) empty_cells.emplace_back(i,j);
        }
    }
    shuffle(empty_cells.begin(), empty_cells.end(), rng);

    vector<int> default_add_list; // [x1, y1, x2, y2, ...]
    // 花の囲い込み
    vector<pair<int,int>> neighbor_cells;
    if(cell_status(tx, ty+1, grid_BB) == "Empty") neighbor_cells = get_neighbor_08(goal);
    else neighbor_cells = get_neighbor_05(goal);

    // 置けるところに置く
    for(auto &cell : neighbor_cells){
        int x = cell.first, y = cell.second;
        if(is_valid(x,y,current_coord,goal,grid_BB,tentative_BB)){
            grid_BB.set(x,y);
            auto it = find(empty_cells.begin(), empty_cells.end(), make_pair(x,y));
            if(it != empty_cells.end()) empty_cells.erase(it);
            default_add_list.push_back(x);
            default_add_list.push_back(y);
        }
    }

    int max_score = -1;
    vector<int> best_add_list = default_add_list;
    vector<pair<int,int>> max_empty_cells = empty_cells;
    BitBoard max_grid_BB = grid_BB;

    int count_try = 0;
    int max_tree_num = (N*N) / 4;
    int cell_swap_num = max_tree_num / 5;
    if(cell_swap_num < 0) cell_swap_num = 0;
    if(cell_swap_num > (int)empty_cells.size()) cell_swap_num = (int)empty_cells.size();

    // 探索ループ
    while(true){
        ++count_try;

        vector<int> add_list = default_add_list;
        BitBoard tmp_grid_BB = grid_BB;
        vector<pair<int,int>> tmp_empty_cells = max_empty_cells;

        // 現在の最短経路集合
        auto path = get_shortest_path(current_coord, goal, tmp_grid_BB);
        unordered_set<int> shortest_path_set;
        shortest_path_set.reserve(path.size()*2 + 8);
        auto idx = [&](int x, int y){ return x*N + y; };
        for(auto &p : path) shortest_path_set.insert(idx(p.first, p.second));

        // ランダムに空きマスを入れ替え
        if(!tmp_empty_cells.empty() && cell_swap_num>0){
            vector<int> idx1(cell_swap_num), idx2(cell_swap_num);
            uniform_int_distribution<int> dist(0, (int)tmp_empty_cells.size()-1);
            for(int i=0;i<cell_swap_num;++i){ idx1[i] = dist(rng); idx2[i] = dist(rng); }
            for(int i=0;i<cell_swap_num;++i){
                swap(tmp_empty_cells[idx1[i]], tmp_empty_cells[idx2[i]]);
            }
        }

        // 木をできるだけ置く（最短経路に干渉しない／干渉しても経路が再構成できるところ）
        int limit = min<int>(max_tree_num, (int)tmp_empty_cells.size());
        for(int i=0;i<limit;++i){
            auto [x,y] = tmp_empty_cells[i];
            auto res = is_valid_11(x,y,current_coord,goal,tmp_grid_BB,tentative_BB,shortest_path_set);
            bool valid = res.first;
            if(valid){
                add_list.push_back(x);
                add_list.push_back(y);
                tmp_grid_BB.set(x,y);
                shortest_path_set = move(res.second);
            }
        }

        int sc = shortest_path_length(current_coord, goal, tmp_grid_BB);
        if(max_score < sc){
            max_score = sc;
            best_add_list = add_list;
            max_grid_BB = tmp_grid_BB;
            max_empty_cells = tmp_empty_cells;
            // cerr << "New best score: " << max_score << "\n";
        }

        if(timer.elapsed() > TIME_LIMIT) break;
    }

    auto add_list = best_add_list;
    grid_BB = max_grid_BB;

    // cerr << "試行回数: " << count_try << "\n";

    // ====== ターン入出力 ======
    // 最初のターン
    {
        int pi, pj; if(!(cin >> pi >> pj)) return 0;
        current_coord = {pi, pj};
        int n; cin >> n;
        for(int k=0;k<n;++k){
            int x,y; cin >> x >> y;
            tentative_BB.set(x,y);
        }
        // (制約上、最初のターンでゴールに到達することはない)
        cout << (int)(add_list.size()/2);
        for(size_t i=0;i<add_list.size(); i+=2){
            cout << ' ' << add_list[i] << ' ' << add_list[i+1];
        }
        cout << "\n" << flush;
    }

    // 以降のターン
    while(true){
        int pi, pj; if(!(cin >> pi >> pj)) return 0;
        pair<int,int> next_coord = {pi, pj};
        int n; cin >> n;
        for(int k=0;k<n;++k){
            int x,y; cin >> x >> y;
            tentative_BB.set(x,y);
        }
        if(next_coord == goal) break;
        cout << 0 << "\n" << flush;
        current_coord = next_coord;
    }
    return 0;
}
