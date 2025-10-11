#include <bits/stdc++.h>
using namespace std;

struct BitBoard {
    int N;
    vector<unsigned long long> b; // (N*N) bits
    BitBoard() {}
    BitBoard(int N_, unsigned long long init=0ULL): N(N_) {
        size_t sz = (size_t(N)*N + 63) / 64;
        b.assign(sz, 0ULL);
        if (init) b[0] = init; // not really used; kept for parity with py ctor
    }
    inline size_t idx(int x, int y) const { return size_t(x)*N + y; }
    inline void set(int x, int y){
        size_t k = idx(x,y);
        b[k>>6] |= (1ULL<<(k&63));
    }
    inline void unset_(int x, int y){
        size_t k = idx(x,y);
        b[k>>6] &= ~(1ULL<<(k&63));
    }
    inline bool is_set(int x, int y) const {
        size_t k = idx(x,y);
        return (b[k>>6] >> (k&63)) & 1ULL;
    }
};

// static const double TIME_LIMIT = 1.8; // 秒（元コードのテスト用設定に合わせる）
static const double TIME_LIMIT = 30.0; // テスト用

// 未使用だが原コードに存在
double eval02(int x, int y, pair<int,int> goal, pair<int,int> start){
    auto [tx,ty]=goal; auto [sx,sy]=start;
    return abs(x-tx)+abs(y-ty)+1e-4*(abs(x-sx)+abs(y-sy));
}

string cell_status(int x, int y, const BitBoard& grid_BB){
    if(!(0<=x && x<grid_BB.N && 0<=y && y<grid_BB.N)) return "Not in grid";
    return grid_BB.is_set(x,y) ? "Tree" : "Empty";
}

bool is_valid(int x, int y,
              pair<int,int> current_coord,
              pair<int,int> goal,
              const BitBoard& grid_BB,
              const BitBoard& tentative_BB)
{
    int N = grid_BB.N;
    if (x<0 || x>=N || y<0 || y>=N) return false;
    if (grid_BB.is_set(x,y)) return false;
    if (make_pair(x,y) == goal) return false;
    if (tentative_BB.is_set(x,y)) return false;

    // BFS: そのマスを木にしたとして current -> goal の経路が存在するか
    deque<pair<int,int>> q;
    vector<char> vis(size_t(N)*N, 0);
    auto enc = [&](int i,int j){ return size_t(i)*N + j; };

    q.emplace_back(current_coord);
    vis[enc(current_coord.first,current_coord.second)] = 1;
    static const int di[4]={-1,1,0,0};
    static const int dj[4]={0,0,-1,1};

    while(!q.empty()){
        auto [cx,cy]=q.front(); q.pop_front();
        if (cx==goal.first && cy==goal.second) return true;
        for(int d=0; d<4; ++d){
            int nx=cx+di[d], ny=cy+dj[d];
            if(0<=nx && nx<N && 0<=ny && ny<N){
                if (!(nx==x && ny==y) && !grid_BB.is_set(nx,ny)) {
                    size_t k = enc(nx,ny);
                    if(!vis[k]){
                        vis[k]=1;
                        q.emplace_back(nx,ny);
                    }
                }
            }
        }
    }
    return false;
}

int shortest_path_length(pair<int,int> start,
                         pair<int,int> goal,
                         const BitBoard& grid_BB)
{
    if (start == goal) return 0;
    int N = grid_BB.N;
    deque<pair<int,int>> q;
    vector<char> vis(size_t(N)*N, 0);
    auto enc = [&](int i,int j){ return size_t(i)*N + j; };

    q.emplace_back(start);
    vis[enc(start.first,start.second)] = 1;

    static const int di[4]={-1,1,0,0};
    static const int dj[4]={0,0,-1,1};
    int dist = 0;

    while(!q.empty()){
        ++dist;
        for(size_t s=q.size(); s>0; --s){
            auto [cx,cy]=q.front(); q.pop_front();
            for(int d=0; d<4; ++d){
                int nx=cx+di[d], ny=cy+dj[d];
                if(0<=nx && nx<N && 0<=ny && ny<N){
                    if (!grid_BB.is_set(nx,ny)) {
                        size_t k = enc(nx,ny);
                        if(!vis[k]){
                            if (nx==goal.first && ny==goal.second) return dist;
                            vis[k]=1;
                            q.emplace_back(nx,ny);
                        }
                    }
                }
            }
        }
    }
    return 1000000000; // 到達不能
}

vector<pair<int,int>> get_neighbor_05(pair<int,int> goal){
    int tx=goal.first, ty=goal.second;
    // (0,-1),(0,1),(-1,0),(1,0) を 2 マスぶん
    vector<pair<int,int>> cells;
    const int dx[4]={0,0,-1,1};
    const int dy[4]={-1,1,0,0};
    for(int k=0;k<4;++k){
        for(int dist=1; dist<=2; ++dist){
            int nx=tx+dx[k]*dist, ny=ty+dy[k]*dist;
            cells.emplace_back(nx,ny);
        }
    }
    return cells;
}

vector<pair<int,int>> get_neighbor_08(pair<int,int> goal){
    int tx=goal.first, ty=goal.second;
    vector<pair<int,int>> cells;
    cells.emplace_back(tx,ty-1);
    cells.emplace_back(tx,ty+1);
    cells.emplace_back(tx-1,ty);
    cells.emplace_back(tx+2,ty);
    cells.emplace_back(tx+1,ty+1);
    cells.emplace_back(tx+1,ty-1);
    return cells;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 乱数・時間
    mt19937 rng(1317);
    auto t_start = chrono::steady_clock::now();

    int N, tx, ty;
    if(!(cin>>N>>tx>>ty)) return 0;
    pair<int,int> goal = {tx, ty};

    vector<string> grid(N);
    for(int i=0;i<N;++i) cin>>grid[i];

    pair<int,int> current_coord = {0, N/2};

    BitBoard grid_BB(N);
    for(int i=0;i<N;++i){
        for(int j=0;j<N;++j){
            if(grid[i][j]=='T') grid_BB.set(i,j);
        }
    }

    BitBoard tentative_BB(N); // 確認済み
    tentative_BB.set(current_coord.first, current_coord.second);

    // 空きマス一覧
    vector<pair<int,int>> empty_cells;
    empty_cells.reserve(N*N);
    for(int i=0;i<N;++i){
        for(int j=0;j<N;++j){
            if(!grid_BB.is_set(i,j)) empty_cells.emplace_back(i,j);
        }
    }

    // 花を囲う（初期配置）
    vector<int> default_add_list;
    vector<pair<int,int>> neighbor_cells;
    if (cell_status(tx, ty+1, grid_BB) == "Empty") {
        neighbor_cells = get_neighbor_08(goal);
    } else {
        neighbor_cells = get_neighbor_05(goal);
    }
    auto erase_empty = [&](int x,int y){
        for(size_t k=0;k<empty_cells.size();++k){
            if (empty_cells[k].first==x && empty_cells[k].second==y){
                empty_cells.erase(empty_cells.begin()+k);
                break;
            }
        }
    };
    for(auto [x,y]: neighbor_cells){
        if (is_valid(x,y,current_coord,goal,grid_BB,tentative_BB)){
            grid_BB.set(x,y);
            erase_empty(x,y);
            default_add_list.push_back(x);
            default_add_list.push_back(y);
        }
    }

    int max_score = -1;
    vector<int> best_add_list = default_add_list;
    BitBoard max_grid_BB = grid_BB;

    int count = 0;
    int max_tree_num = (N*N)/4;

    // 探索ループ
    while(true){
        ++count;
        shuffle(empty_cells.begin(), empty_cells.end(), rng);

        vector<int> add_list = default_add_list;
        BitBoard tmp_grid_BB = grid_BB;

        for(int i=0; i<max_tree_num && i<(int)empty_cells.size(); ++i){
            auto [x,y] = empty_cells[i];
            if (is_valid(x,y,current_coord,goal,tmp_grid_BB,tentative_BB)){
                add_list.push_back(x);
                add_list.push_back(y);
                tmp_grid_BB.set(x,y);
            }
        }

        int initial_path_length = shortest_path_length(current_coord, goal, tmp_grid_BB);

        if (max_score < initial_path_length){
            max_score = initial_path_length;
            best_add_list = add_list;
            max_grid_BB = tmp_grid_BB;
            // cerr << "New best score: " << max_score << "\n";
        }

        auto now = chrono::steady_clock::now();
        double elapsed = chrono::duration<double>(now - t_start).count();
        if (elapsed > TIME_LIMIT) break;
    }

    vector<int> add_list = best_add_list;
    grid_BB = max_grid_BB;

    // cerr << "試行回数: " << count << "\n";

    // --- 以降は対話 (最初のターン) ---
    // 次に移動する座標
    int next_pi, next_pj;
    if(!(cin >> next_pi >> next_pj)) return 0;
    // 新たに確認済みとなったマス
    int n; cin >> n;
    for(int k=0;k<n;++k){
        int x,y; cin>>x>>y;
        tentative_BB.set(x,y);
    }

    // 初回の配置出力
    cout << (add_list.size()/2);
    for(size_t i=0;i<add_list.size(); i+=2){
        cout << ' ' << add_list[i] << ' ' << add_list[i+1];
    }
    cout << '\n' << flush;
    current_coord = {next_pi, next_pj};

    // --- 2ターン目以降 ---
    while(true){
        if(!(cin >> next_pi >> next_pj)) break;
        cin >> n;
        for(int k=0;k<n;++k){
            int x,y; cin>>x>>y;
            tentative_BB.set(x,y);
        }
        if (next_pi==goal.first && next_pj==goal.second){
            break;
        }
        cout << 0 << '\n' << flush;
        current_coord = {next_pi, next_pj};
    }
    return 0;
}
