#include <bits/stdc++.h>
using namespace std;

struct BitBoard {
  int N;                 // board is N x N
  int M;                 // total cells = N*N
  vector<unsigned long long> bits;

  BitBoard() : N(0), M(0) {}
  BitBoard(int n) : N(n), M(n*n), bits((M + 63) >> 6, 0ULL) {}

  void reset(int n) {
    N = n; M = n*n;
    bits.assign((M + 63) >> 6, 0ULL);
  }

  inline int idx(int x, int y) const { return x * N + y; }

  inline void set(int x, int y) {
    int k = idx(x, y);
    bits[k >> 6] |= (1ULL << (k & 63));
  }
  inline void unset(int x, int y) {
    int k = idx(x, y);
    bits[k >> 6] &= ~(1ULL << (k & 63));
  }
  inline bool is_set(int x, int y) const {
    int k = idx(x, y);
    return (bits[k >> 6] >> (k & 63)) & 1ULL;
  }
};

static inline bool in_bounds(int x, int y, int N) {
  return (0 <= x && x < N && 0 <= y && y < N);
}

bool is_valid(int x, int y,
              const pair<int,int>& current_coord,
              const pair<int,int>& goal,
              const BitBoard& grid_BB,
              const BitBoard& tentative_BB)
{
  int N = grid_BB.N;
  // 範囲外
  if (!in_bounds(x, y, N)) return false;
  // 既に木
  if (grid_BB.is_set(x, y)) return false;
  // ゴールは不可
  if (make_pair(x, y) == goal) return false;
  // 確認済みマスに木は置けない
  if (tentative_BB.is_set(x, y)) return false;

  // (x,y) を木にしたと仮定して、現在地→ゴールに到達可能か判定 (BFS)
  queue<pair<int,int>> q;
  BitBoard visited(N);
  q.push(current_coord);
  visited.set(current_coord.first, current_coord.second);

  static const int dx[4] = {-1, 1,  0, 0};
  static const int dy[4] = { 0, 0, -1, 1};

  while (!q.empty()) {
    auto [cx, cy] = q.front(); q.pop();
    if (make_pair(cx, cy) == goal) return true;
    for (int dir = 0; dir < 4; ++dir) {
      int nx = cx + dx[dir], ny = cy + dy[dir];
      if (!in_bounds(nx, ny, N)) continue;
      if (grid_BB.is_set(nx, ny)) continue;
      if (visited.is_set(nx, ny)) continue;
      // ここに今回新しく置く木がある想定
      if (nx == x && ny == y) continue;
      visited.set(nx, ny);
      q.emplace(nx, ny);
    }
  }
  return false;
}

int shortest_path_length(const pair<int,int>& start,
                         const pair<int,int>& goal,
                         const BitBoard& grid_BB)
{
  if (start == goal) return 0;
  int N = grid_BB.N;
  deque<pair<int,int>> dq;
  dq.push_back(start);

  BitBoard visited(N);
  visited.set(start.first, start.second);

  static const int dx[4] = {-1, 1,  0, 0};
  static const int dy[4] = { 0, 0, -1, 1};

  int dist = 0;
  while (!dq.empty()) {
    ++dist;
    int qs = (int)dq.size();
    for (int _ = 0; _ < qs; ++_) {
      auto [cx, cy] = dq.front(); dq.pop_front();
      for (int dir = 0; dir < 4; ++dir) {
        int nx = cx + dx[dir], ny = cy + dy[dir];
        if (!in_bounds(nx, ny, N)) continue;
        if (grid_BB.is_set(nx, ny)) continue;
        if (visited.is_set(nx, ny)) continue;
        if (make_pair(nx, ny) == goal) return dist;
        visited.set(nx, ny);
        dq.emplace_back(nx, ny);
      }
    }
  }
  return 1000000000; // unreachable
}

vector<pair<int,int>> get_neighbor_05(const pair<int,int>& goal) {
  int tx = goal.first, ty = goal.second;
  // (0,-1),(0,1),(-1,0),(1,0) の順に、距離 1..2
  static const int dx[4] = {0, 0, -1, 1};
  static const int dy[4] = {-1, 1, 0, 0};
  vector<pair<int,int>> cells;
  for (int d = 0; d < 4; ++d) {
    for (int dist = 1; dist <= 2; ++dist) {
      int nx = tx + dx[d] * dist;
      int ny = ty + dy[d] * dist;
      cells.emplace_back(nx, ny);
    }
  }
  return cells;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  // 乱数
  mt19937 rng(1317);

  // 時間計測
  using Clock = chrono::steady_clock;
  auto start_time = Clock::now();
  const double TIME_LIMIT = 1.8; // 秒（必要に応じて調整）

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

  BitBoard tentative_BB(N); // 確認済みマス
  tentative_BB.set(current_coord.first, current_coord.second);

  // 空きマス一覧
  vector<pair<int,int>> empty_cells;
  empty_cells.reserve(N*N);
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      if (!grid_BB.is_set(i, j)) empty_cells.emplace_back(i, j);
    }
  }

  // 初期で花の近傍に木を置く（有効なもののみ）
  vector<int> default_add_list; // [x1, y1, x2, y2, ...]
  auto neighbor_cells = get_neighbor_05(goal);
  for (auto [x, y] : neighbor_cells) {
    if (is_valid(x, y, current_coord, goal, grid_BB, tentative_BB)) {
      grid_BB.set(x, y);
      // Python版では empty_cells.remove をしていたが、後段の is_valid が弾くので必須ではない
      default_add_list.push_back(x);
      default_add_list.push_back(y);
    }
  }

  int max_score = -1;
  vector<int> best_add_list = default_add_list;
  BitBoard max_grid_BB = grid_BB;

  int count_trials = 0;
  int max_tree_num = (N * N) / 4;  // 追加木の最大数（ヒューリスティック）

  // 時間の許す限り、ランダムに追加候補を作って最短距離が最大の構成を探す
  while (true) {
    ++count_trials;

    shuffle(empty_cells.begin(), empty_cells.end(), rng);

    vector<int> add_list = default_add_list;
    BitBoard tmp_grid_BB = grid_BB;

    for (int i = 0; i < (int)empty_cells.size() && i < max_tree_num; ++i) {
      auto [x, y] = empty_cells[i];
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
      // cerr << "New best score: " << max_score << "\n";
    }

    // タイムリミット判定
    auto now = Clock::now();
    double elapsed = chrono::duration<double>(now - start_time).count();
    if (elapsed > TIME_LIMIT) break;
  }

  vector<int> add_list = best_add_list;
  BitBoard final_grid_BB = max_grid_BB;

  // cerr << "試行回数: " << count_trials << "\n";

  // === 以降は対話パート ===

  // 最初のターンの入力
  {
    int pi, pj;
    if (!(cin >> pi >> pj)) return 0;
    int n; cin >> n;
    for (int k = 0; k < n; ++k) {
      int x, y; cin >> x >> y;
      tentative_BB.set(x, y);
    }

    // 追加する木の出力
    int m = (int)add_list.size() / 2;
    cout << m;
    for (int v : add_list) cout << ' ' << v;
    cout << '\n' << flush;

    current_coord = {pi, pj};
  }

  // 2ターン目以降
  while (true) {
    int pi, pj;
    if (!(cin >> pi >> pj)) return 0;
    int n; cin >> n;
    for (int k = 0; k < n; ++k) {
      int x, y; cin >> x >> y;
      tentative_BB.set(x, y);
    }
    if (make_pair(pi, pj) == goal) {
      // 到達で終了
      break;
    }
    // 以降は木を追加しない
    cout << 0 << '\n' << flush;
    current_coord = {pi, pj};
  }

  return 0;
}
