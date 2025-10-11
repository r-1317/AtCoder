#include <bits/stdc++.h>
using namespace std;

/*** 乱数・時間 ***/
static const uint32_t RNG_SEED = 1317;
static constexpr double TIME_LIMIT_SECONDS = 1.9;
mt19937 rng(RNG_SEED);
inline double now_sec() {
  static const auto t0 = chrono::steady_clock::now();
  auto t = chrono::steady_clock::now();
  return chrono::duration<double>(t - t0).count();
}

/*** BitBoard（任意サイズ N×N をビット配列で管理） ***/
struct BitBoard {
  int N;
  vector<uint64_t> bits; // 64bit チャンク

  BitBoard() {}
  BitBoard(int N_, uint64_t fill = 0) : N(N_) {
    int total = N * N;
    int chunks = (total + 63) >> 6;
    bits.assign(chunks, 0ULL);
    if (fill) { /* 未使用（Python版と整合のための引数だけ保持） */ }
  }
  inline int idx(int x, int y) const { return x * N + y; }
  inline void set(int x, int y) {
    int p = idx(x, y);
    bits[p >> 6] |= (1ULL << (p & 63));
  }
  inline void unset(int x, int y) {
    int p = idx(x, y);
    bits[p >> 6] &= ~(1ULL << (p & 63));
  }
  inline bool is_set(int x, int y) const {
    int p = idx(x, y);
    return (bits[p >> 6] >> (p & 63)) & 1ULL;
  }
};

/*** ユーティリティ ***/
struct PairHash {
  size_t operator()(const pair<int,int>& p) const noexcept {
    return (static_cast<size_t>(p.first) << 32) ^ static_cast<size_t>(p.second);
  }
};

static const int DX[4] = {-1, 1, 0, 0};
static const int DY[4] = {0, 0, -1, 1};

/*** 最短距離（木マスは通れない） ***/
int shortest_path_length(pair<int,int> start, pair<int,int> goal, const BitBoard& grid) {
  if (start == goal) return 0;
  int N = grid.N;
  queue<pair<int,int>> q;
  BitBoard vis(N);
  q.push(start);
  vis.set(start.first, start.second);
  int dist = 0;
  while (!q.empty()) {
    int qs = (int)q.size();
    ++dist;
    while (qs--) {
      auto [x, y] = q.front(); q.pop();
      for (int d = 0; d < 4; ++d) {
        int nx = x + DX[d], ny = y + DY[d];
        if (nx < 0 || nx >= N || ny < 0 || ny >= N) continue;
        if (!grid.is_set(nx, ny) && !vis.is_set(nx, ny)) {
          if (nx == goal.first && ny == goal.second) return dist;
          vis.set(nx, ny);
          q.emplace(nx, ny);
        }
      }
    }
  }
  return (int)1e9; // 到達不能
}

/*** (x,y) に木を追加してもよいか判定（出口からゴールまでの経路が残るか等） ***/
bool is_valid(int x, int y,
              const pair<int,int>& current_coord,
              const pair<int,int>& goal,
              const BitBoard& grid_BB,
              const BitBoard& tentative_BB) {
  int N = grid_BB.N;
  if (x < 0 || x >= N || y < 0 || y >= N) return false;
  if (grid_BB.is_set(x, y)) return false;
  if (x == goal.first && y == goal.second) return false;
  if (tentative_BB.is_set(x, y)) return false;

  // (x,y) を木にすると仮定し、current から goal へ到達可能かBFS
  queue<pair<int,int>> q;
  BitBoard vis(N);
  q.push(current_coord);
  vis.set(current_coord.first, current_coord.second);

  while (!q.empty()) {
    auto [cx, cy] = q.front(); q.pop();
    if (cx == goal.first && cy == goal.second) return true;
    for (int d = 0; d < 4; ++d) {
      int nx = cx + DX[d], ny = cy + DY[d];
      if (nx < 0 || nx >= N || ny < 0 || ny >= N) continue;
      if ((nx == x && ny == y)) continue;            // ここに新たに木を置く
      if (!grid_BB.is_set(nx, ny) && !vis.is_set(nx, ny)) {
        vis.set(nx, ny);
        q.emplace(nx, ny);
      }
    }
  }
  return false;
}

/*** 近傍生成（Pythonの get_neighbor_05 / get_neighbor_08 と同等） ***/
vector<pair<int,int>> get_neighbor_05(const pair<int,int>& goal) {
  int tx = goal.first, ty = goal.second;
  // directions = [(0,-1),(0,1),(-1,0),(1,0)]、各 dist=1..2
  static const int dirs[4][2] = {{0,-1},{0,1},{-1,0},{1,0}};
  vector<pair<int,int>> cells;
  for (auto &d : dirs) {
    for (int dist = 1; dist <= 2; ++dist) {
      int nx = tx + d[0]*dist, ny = ty + d[1]*dist;
      cells.emplace_back(nx, ny);
    }
  }
  return cells;
}

vector<pair<int,int>> get_neighbor_08(const pair<int,int>& goal) {
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

/*** (x,y) の状態（盤外は Not in grid 扱い、Pythonの挙動と整合） ***/
enum CellState { NotInGrid = 0, Empty = 1, Tree = 2 };
CellState cell_status(int x, int y, const BitBoard& grid_BB) {
  int N = grid_BB.N;
  if (x < 0 || x >= N || y < 0 || y >= N) return NotInGrid;
  return grid_BB.is_set(x, y) ? Tree : Empty;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int N, tx, ty;
  if (!(cin >> N >> tx >> ty)) return 0;
  pair<int,int> goal = {tx, ty};

  vector<string> grid(N);
  for (int i = 0; i < N; ++i) cin >> grid[i];

  pair<int,int> current_coord = {0, N/2};

  BitBoard grid_BB(N);
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      if (grid[i][j] == 'T') grid_BB.set(i, j);
    }
  }

  BitBoard tentative_BB(N);
  tentative_BB.set(current_coord.first, current_coord.second);

  // 空きマス一覧
  vector<pair<int,int>> empty_cells;
  empty_cells.reserve(N*N);
  for (int i = 0; i < N; ++i) for (int j = 0; j < N; ++j) {
    if (!grid_BB.is_set(i, j)) empty_cells.emplace_back(i, j);
  }
  shuffle(empty_cells.begin(), empty_cells.end(), rng);

  // 出力用に [x1, y1, x2, y2, ...]
  vector<int> default_add_list;

  // 花の周囲を囲う（Pythonの分岐に合わせる）
  vector<pair<int,int>> neighbor_cells;
  if (cell_status(tx, ty+1, grid_BB) == Empty) {
    neighbor_cells = get_neighbor_08(goal);
  } else {
    neighbor_cells = get_neighbor_05(goal);
  }
  for (auto [x, y] : neighbor_cells) {
    if (is_valid(x, y, current_coord, goal, grid_BB, tentative_BB)) {
      grid_BB.set(x, y);
      // empty_cells から (x,y) を除去
      auto it = find(empty_cells.begin(), empty_cells.end(), make_pair(x, y));
      if (it != empty_cells.end()) empty_cells.erase(it);
      default_add_list.push_back(x);
      default_add_list.push_back(y);
    }
  }

  int max_score = -1;
  vector<int> best_add_list = default_add_list;
  vector<pair<int,int>> max_empty_cells = empty_cells;
  BitBoard max_grid_BB = grid_BB;

  int count_try = 0;
  int max_tree_num = (N * N) / 4;           // N^2 / 4
  int cell_swap_num = max_tree_num / 5;     // その 1/5

  // 探索ループ
  while (true) {
    ++count_try;
    vector<int> add_list = default_add_list;
    BitBoard tmp_grid_BB = grid_BB;
    vector<pair<int,int>> tmp_empty_cells = max_empty_cells;

    // 空きマスをランダムに入れ替える（Pythonの random.sample + swap と同等の効果）
    if (!tmp_empty_cells.empty() && cell_swap_num > 0) {
      uniform_int_distribution<int> dist(0, (int)tmp_empty_cells.size()-1);
      vector<int> idx1(cell_swap_num), idx2(cell_swap_num);
      for (int i = 0; i < cell_swap_num; ++i) {
        idx1[i] = dist(rng);
        idx2[i] = dist(rng);
        swap(tmp_empty_cells[idx1[i]], tmp_empty_cells[idx2[i]]);
      }
    }

    int limit = min((int)tmp_empty_cells.size(), max_tree_num);
    for (int i = 0; i < limit; ++i) {
      auto [x, y] = tmp_empty_cells[i];
      if (is_valid(x, y, current_coord, goal, tmp_grid_BB, tentative_BB)) {
        add_list.push_back(x);
        add_list.push_back(y);
        tmp_grid_BB.set(x, y);
      }
    }

    int initial_path_length = shortest_path_length(current_coord, goal, tmp_grid_BB);
    if (max_score < initial_path_length) {
      max_score = initial_path_length;
      best_add_list = add_list;
      max_grid_BB = tmp_grid_BB;
      max_empty_cells = tmp_empty_cells;
      // cerr << "New best score: " << max_score << "\n";
    }

    if (now_sec() > TIME_LIMIT_SECONDS) break;
  }

  vector<int> add_list = best_add_list;
  grid_BB = max_grid_BB;

  // cerr << "試行回数: " << count_try << "\n";

  // --- 最初のターン ---
  {
    int pi, pj; 
    cin >> pi >> pj; // 次に移動する座標
    int n; 
    cin >> n;        // 新規確認マス数
    for (int k = 0; k < n; ++k) {
      int x, y; cin >> x >> y;
      tentative_BB.set(x, y);
    }
    // 配置する木を出力
    cout << (int)(add_list.size() / 2);
    for (size_t i = 0; i < add_list.size(); i += 2) {
      cout << ' ' << add_list[i] << ' ' << add_list[i+1];
    }
    cout << '\n' << flush;
    current_coord = {pi, pj};
  }

  // --- 以降のターン ---
  while (true) {
    int pi, pj;
    if (!(cin >> pi >> pj)) break; // 念のため
    int n; 
    cin >> n;
    for (int k = 0; k < n; ++k) {
      int x, y; cin >> x >> y;
      tentative_BB.set(x, y);
    }
    if (pi == tx && pj == ty) {
      // ゴール到達
      break;
    }
    cout << 0 << '\n' << flush; // 追加配置なし
    current_coord = {pi, pj};
  }

  return 0;
}
