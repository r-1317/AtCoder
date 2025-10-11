// g++ -std=gnu++17 -O2 -pipe -static -s -o Main Main.cpp
#include <bits/stdc++.h>
using namespace std;

struct BitBoard {
    int N;
    vector<unsigned long long> bits; // dynamic bitset
    BitBoard(int n = 0, unsigned long long fill = 0ULL) : N(n) {
        int sz = (N * N + 63) >> 6;
        bits.assign(sz, 0ULL);
        if (fill) bits[0] = fill; // unused; kept for parity with Py ctor
    }
    void set(int x, int y) {
        int id = x * N + y;
        bits[id >> 6] |= (1ULL << (id & 63));
    }
    void unset(int x, int y) {
        int id = x * N + y;
        bits[id >> 6] &= ~(1ULL << (id & 63));
    }
    bool is_set(int x, int y) const {
        int id = x * N + y;
        return (bits[id >> 6] >> (id & 63)) & 1ULL;
    }
};

// Manhattan + small tie-break (unused elsewhere but ported for completeness)
static inline double eval02(int x, int y, pair<int,int> goal, pair<int,int> start){
    auto [tx,ty]=goal; auto [sx,sy]=start;
    return abs(x-tx)+abs(y-ty)+1e-4*(abs(x-sx)+abs(y-sy));
}

bool is_valid(int x, int y,
              const pair<int,int>& current_coord,
              const pair<int,int>& goal,
              const BitBoard& grid_BB,
              const BitBoard& tentative_BB)
{
    int N = grid_BB.N;
    // bounds
    if (x < 0 || x >= N || y < 0 || y >= N) return false;
    // already tree
    if (grid_BB.is_set(x, y)) return false;
    // cannot place on goal
    if (make_pair(x, y) == goal) return false;
    // cannot place on confirmed cell
    if (tentative_BB.is_set(x, y)) return false;

    // BFS on grid_BB with an extra blocked cell (x,y)
    queue<pair<int,int>> q;
    BitBoard visited(N);
    q.emplace(current_coord);
    visited.set(current_coord.first, current_coord.second);

    static const int di[4] = {-1,1,0,0};
    static const int dj[4] = {0,0,-1,1};

    while(!q.empty()){
        auto [cx, cy] = q.front(); q.pop();
        if (make_pair(cx, cy) == goal) return true;
        for(int dir=0; dir<4; ++dir){
            int nx = cx + di[dir], ny = cy + dj[dir];
            if (0 <= nx && nx < N && 0 <= ny && ny < N){
                if (!grid_BB.is_set(nx, ny) && !visited.is_set(nx, ny) &&
                    !(nx == x && ny == y)) {
                    visited.set(nx, ny);
                    q.emplace(nx, ny);
                }
            }
        }
    }
    return false; // no path to goal
}

int shortest_path_length(const pair<int,int>& start,
                         const pair<int,int>& goal,
                         const BitBoard& grid_BB)
{
    if (start == goal) return 0;
    int N = grid_BB.N;
    queue<pair<int,int>> q;
    BitBoard visited(N);
    q.emplace(start);
    visited.set(start.first, start.second);

    static const int di[4] = {-1,1,0,0};
    static const int dj[4] = {0,0,-1,1};

    int dist = 0;
    while(!q.empty()){
        ++dist;
        int qs = (int)q.size();
        for(int _=0; _<qs; ++_){
            auto [cx, cy] = q.front(); q.pop();
            for(int dir=0; dir<4; ++dir){
                int nx = cx + di[dir], ny = cy + dj[dir];
                if (0 <= nx && nx < N && 0 <= ny && ny < N){
                    if (!grid_BB.is_set(nx, ny) && !visited.is_set(nx, ny)){
                        if (make_pair(nx, ny) == goal) return dist;
                        visited.set(nx, ny);
                        q.emplace(nx, ny);
                    }
                }
            }
        }
    }
    return 1000000000; // unreachable
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Fixed seed as in Python (random.seed(1317))
    mt19937 rng(1317);

    auto start_clock = chrono::steady_clock::now();
    const double TIME_LIMIT = 1.85; // seconds (change to 50.0 for local testing)

    int N, tx, ty;
    if(!(cin >> N >> tx >> ty)) return 0;
    pair<int,int> goal = {tx, ty};

    vector<string> grid(N);
    for(int i=0;i<N;i++) cin >> grid[i];

    pair<int,int> current_coord = {0, N/2};

    BitBoard grid_BB(N);
    for(int i=0;i<N;i++){
        for(int j=0;j<N;j++){
            if(grid[i][j] == 'T') grid_BB.set(i,j);
        }
    }

    BitBoard tentative_BB(N); // confirmed cells
    tentative_BB.set(current_coord.first, current_coord.second);

    // collect all empty cells
    vector<pair<int,int>> empty_cells;
    empty_cells.reserve(N*N);
    for(int i=0;i<N;i++){
        for(int j=0;j<N;j++){
            if(!grid_BB.is_set(i,j)) empty_cells.emplace_back(i,j);
        }
    }

    int max_score = -1;
    vector<int> best_add_list; // flat [x1, y1, x2, y2, ...]
    BitBoard max_grid_BB(N);
    max_grid_BB.bits = grid_BB.bits;

    int count = 0;

    while(true){
        ++count;

        // shuffle
        shuffle(empty_cells.begin(), empty_cells.end(), rng);

        vector<int> add_list;
        BitBoard tmp_grid_BB(N);
        tmp_grid_BB.bits = grid_BB.bits;

        // try to place up to 100 trees
        for(int i=0; i<(int)empty_cells.size() && i<100; ++i){
            auto [x, y] = empty_cells[i];
            if (is_valid(x, y, current_coord, goal, tmp_grid_BB, tentative_BB)){
                add_list.push_back(x);
                add_list.push_back(y);
                tmp_grid_BB.set(x, y);
            }
        }

        // evaluate by shortest path length from current to goal
        int initial_path_length = shortest_path_length(current_coord, goal, tmp_grid_BB);

        if (max_score < initial_path_length){
            max_score = initial_path_length;
            best_add_list = add_list;
            max_grid_BB.bits = tmp_grid_BB.bits;
            cerr << "New best score: " << max_score << "\n";
        }

        // time check
        auto now = chrono::steady_clock::now();
        double elapsed = chrono::duration<double>(now - start_clock).count();
        if (elapsed > TIME_LIMIT) break;
    }

    vector<int> add_list = best_add_list;
    grid_BB.bits = max_grid_BB.bits;

    cerr << "試行回数: " << count << "\n";

    // ===== Turn 1 =====
    int pi, pj; // next position
    if(!(cin >> pi >> pj)) return 0;
    int n; cin >> n;
    for(int k=0;k<n;k++){
        int x,y; cin >> x >> y;
        tentative_BB.set(x,y);
    }
    // output placements
    cout << (int)(add_list.size()/2);
    for(size_t i=0;i<add_list.size();i++){
        cout << ' ' << add_list[i];
    }
    cout << '\n' << flush;
    current_coord = {pi, pj};

    // ===== Subsequent turns =====
    while(true){
        if(!(cin >> pi >> pj)) break; // safety
        int n2; cin >> n2;
        for(int k=0;k<n2;k++){
            int x,y; cin >> x >> y;
            tentative_BB.set(x,y);
        }
        if (make_pair(pi, pj) == goal) break;
        cout << 0 << '\n' << flush;
        current_coord = {pi, pj};
    }

    return 0;
}
