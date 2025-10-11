#include <bits/stdc++.h>
using namespace std;

/*** 設定 ***/
static const unsigned SEED = 1317;
// static const double TIME_LIMIT_SEC = 50.0;   // Pythonコードに合わせてテスト用 50 秒
static const double TIME_LIMIT_SEC = 1.8; // 本番想定ならこちら

/*** BitBoard 実装（N*N <= 1600 ビット） ***/
struct BitBoard {
  int N;
  vector<uint64_t> bits; // 64bit チャンク
  BitBoard() {}
  BitBoard(int n, uint64_t init_val = 0ULL) : N(n) {
    size_t sz = (size_t(n)*n + 63) / 64;
    bits.assign(sz, 0ULL);
    if (init_val != 0ULL) bits[0] = init_val; // 互換用（基本は 0 初期化）
  }
  inline size_t idx(int x, int y) const { return (size_t)x * N + y; }
  inline void set(int x, int y) {
    size_t t = idx(x, y);
    bits[t >> 6] |= (1ULL << (t & 63));
  }
  inline void unset(int x, int y) {
    size_t t = idx(x, y);
    bits[t >> 6] &= ~(1ULL << (t & 63));
  }
  inline bool is_set(int x, int y) const {
    size_t t = idx(x, y);
    return (bits[t >> 6] >> (t & 63)) & 1ULL;
  }
};

/*** 便利 ***/
struct Coord { int x, y; };

static inline double eval02(int x, int y, pair<int,int> goal, pair<int,int> start){
  int tx = goal.first, ty = goal.second;
  int sx = start.first, sy = start.second;
  return abs(x - tx) + abs(y - ty) + 1e-4 * (abs(x - sx) + abs(y - sy));
}

static inline bool in_grid(int x, int y, int N){
  return (0 <= x && x < N && 0 <= y && y < N);
}

/*** (x,y) に木を追加して良いか（制約 & 現在地→ゴールの経路が残るか） ***/
bool is_valid_place(int x, int y,
                    pair<int,int> current_coord,
                    pair<int,int> goal,
                    const BitBoard &grid_BB,
                    const BitBoard &tentative_BB)
{
  int N = grid_BB.N;
  if (!in_grid(x, y, N)) return false;
  if (grid_BB.is_set(x, y)) return false;
  if (make_pair(x, y) == goal) return false;
  if (tentative_BB.is_set(x, y)) return false;

  // (x,y) を木にすると仮定して、現在地→ゴールの到達可能性を BFS で確認
  deque<pair<int,int>> q;
  BitBoard visited(N);
  q.emplace_back(current_coord);
  visited.set(current_coord.first, current_coord.second);
  static const int dx[4] = {-1, 1, 0, 0};
  static const int dy[4] = {0, 0, -1, 1};

  while(!q.empty()){
    auto [cx, cy] = q.front(); q.pop_front();
    if (cx == goal.first && cy == goal.second) return true;
    for (int dir = 0; dir < 4; ++dir){
      int nx = cx + dx[dir], ny = cy + dy[dir];
      if (!in_grid(nx, ny, N)) continue;
      if (grid_BB.is_set(nx, ny)) continue;
      if (nx == x && ny == y) continue; // ここに木を置いたと仮定
      if (visited.is_set(nx, ny)) continue;
      visited.set(nx, ny);
      q.emplace_back(nx, ny);
    }
  }
  return false;
}

/*** 最短経路長（木は通れない）。到達不能なら 1e9 ***/
int shortest_path_length(pair<int,int> start,
                         pair<int,int> goal,
                         const BitBoard &grid_BB)
{
  if (start == goal) return 0;
  int N = grid_BB.N;
  deque<pair<int,int>> q;
  BitBoard visited(N);
  visited.set(start.first, start.second);
  q.emplace_back(start);
  static const int dx[4] = {-1, 1, 0, 0};
  static const int dy[4] = {0, 0, -1, 1};
  int dist = 0;

  while (!q.empty()){
    ++dist;
    int qs = (int)q.size();
    for (int _=0; _<qs; ++_){
      auto [cx, cy] = q.front(); q.pop_front();
      for (int dir = 0; dir < 4; ++dir){
        int nx = cx + dx[dir], ny = cy + dy[dir];
        if (!in_grid(nx, ny, N)) continue;
        if (grid_BB.is_set(nx, ny)) continue;
        if (visited.is_set(nx, ny)) continue;
        if (nx == goal.first && ny == goal.second) return dist;
        visited.set(nx, ny);
        q.emplace_back(nx, ny);
      }
    }
  }
  return 1000000000; // 1e9
}

/*** 近傍（Pythonの get_neighbor_05 と get_neighbor_08 を再現） ***/
vector<pair<int,int>> get_neighbor_05(pair<int,int> goal){
  int tx = goal.first, ty = goal.second;
  // directions = [(0,-1),(0,1),(-1,0),(1,0)] with dist in {1,2}
  static const int dirs[4][2] = {{0,-1},{0,1},{-1,0},{1,0}};
  vector<pair<int,int>> cells;
  for (auto &d : dirs){
    for (int dist = 1; dist <= 2; ++dist){
      int nx = tx + d[0]*dist, ny = ty + d[1]*dist;
      cells.emplace_back(nx, ny);
    }
  }
  return cells;
}

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

string cell_status(int x, int y, const BitBoard &grid_BB){
  if (!in_grid(x, y, grid_BB.N)) return "Not in grid";
  return grid_BB.is_set(x,y) ? "Tree" : "Empty";
}

int main(){
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  // 乱数初期化
  std::mt19937 rng(SEED);
  std::uniform_real_distribution<double> urand(0.0, 1.0);

  int N, tx, ty;
  if (!(cin >> N >> tx >> ty)) return 0;
  pair<int,int> goal = {tx, ty};

  vector<string> grid(N);
  for (int i=0;i<N;i++) cin >> grid[i];

  pair<int,int> current_coord = {0, N/2};

  BitBoard grid_BB(N);
  for (int i=0;i<N;i++){
    for (int j=0;j<N;j++){
      if (grid[i][j] == 'T') grid_BB.set(i,j);
    }
  }

  BitBoard tentative_BB(N);
  tentative_BB.set(current_coord.first, current_coord.second);

  // 空きマス一覧
  vector<pair<int,int>> empty_cells;
  empty_cells.reserve(N*N);
  for (int i=0;i<N;i++){
    for (int j=0;j<N;j++){
      if (!grid_BB.is_set(i,j)) empty_cells.emplace_back(i,j);
    }
  }

  // ランダムシャッフル
  shuffle(empty_cells.begin(), empty_cells.end(), rng);

  vector<int> default_add_list; // [x1, y1, x2, y2, ...]
  // 花を囲う（Python の条件分岐を踏襲）
  vector<pair<int,int>> neighbor_cells;
  if (cell_status(tx, ty+1, grid_BB) == "Empty"){
    neighbor_cells = get_neighbor_08(goal);
  } else {
    neighbor_cells = get_neighbor_05(goal);
  }
  for (auto &cell : neighbor_cells){
    int x = cell.first, y = cell.second;
    if (is_valid_place(x, y, current_coord, goal, grid_BB, tentative_BB)){
      grid_BB.set(x, y);
      auto it = find(empty_cells.begin(), empty_cells.end(), cell);
      if (it != empty_cells.end()) empty_cells.erase(it);
      default_add_list.push_back(x);
      default_add_list.push_back(y);
    }
  }

  int max_score = -1;
  vector<int> best_add_list = default_add_list;
  vector<pair<int,int>> max_empty_cells = empty_cells;
  BitBoard max_grid_BB = grid_BB;

  long long count = 0;
  int max_tree_num = (N*N) / 4;
  int cell_swap_num = max_tree_num / 5;

  double temperature = 1000.0;
  const double cooling_rate = 0.990;

  auto time_start = chrono::steady_clock::now();

  while (true){
    ++count;

    vector<int> add_list = default_add_list;          // 出力候補
    BitBoard tmp_grid_BB = grid_BB;                  // 盤複製
    vector<pair<int,int>> tmp_empty_cells = max_empty_cells; // 空き複製

    // ランダムに入れ替え（Python: random.sample 2 回 → 対応として 2 つのシャッフルから先頭 cell_swap_num を使用）
    if (!tmp_empty_cells.empty() && cell_swap_num > 0){
      vector<int> idx(tmp_empty_cells.size());
      iota(idx.begin(), idx.end(), 0);

      auto idx1 = idx, idx2 = idx;
      shuffle(idx1.begin(), idx1.end(), rng);
      shuffle(idx2.begin(), idx2.end(), rng);
      int k = min<int>(cell_swap_num, (int)tmp_empty_cells.size());
      for (int i=0;i<k;i++){
        int a = idx1[i], b = idx2[i];
        if (a == b) continue;
        swap(tmp_empty_cells[a], tmp_empty_cells[b]);
      }
    }

    // できるだけ多く木を置く（最大 max_tree_num 回試行）
    for (int i=0; i<max_tree_num && i<(int)tmp_empty_cells.size(); ++i){
      auto cell = tmp_empty_cells[i];
      int x = cell.first, y = cell.second;
      if (is_valid_place(x, y, current_coord, goal, tmp_grid_BB, tentative_BB)){
        add_list.push_back(x);
        add_list.push_back(y);
        tmp_grid_BB.set(x, y);
      }
    }

    // スコア（入口→花の最短路長）
    int score = shortest_path_length(current_coord, goal, tmp_grid_BB);

    // 0.01 の確率でデバッグ表示（stderr）
    if (urand(rng) < 0.01){
      double prob = exp((double)(score - max_score) / max(1e-9, temperature));
      // cerr << prob << "\n";
      // cerr << "温度: " << temperature << "\n";
    }

    // ベター or 焼きなまし受理
    double accept_prob = exp((double)(score - max_score) / max(1e-9, temperature));
    if (score > max_score || urand(rng) < accept_prob){
      max_score = score;
      best_add_list = add_list;
      max_grid_BB = tmp_grid_BB;
      max_empty_cells = tmp_empty_cells;
    }

    // 冷却
    temperature *= cooling_rate;

    // 時間終了
    auto now = chrono::steady_clock::now();
    double elapsed = chrono::duration<double>(now - time_start).count();
    if (elapsed > TIME_LIMIT_SEC) break;
  }

  auto add_list = best_add_list;
  grid_BB = max_grid_BB;

  // cerr << "試行回数: " << count << "\n";

  // --- 以降は対話 I/O ---

  // 最初のターン入力
  int pi, pj; // 次に移動する座標
  if (!(cin >> pi >> pj)) return 0;
  int n;      // 新たに確認済みになったマス数
  if (!(cin >> n)) return 0;
  for (int k=0;k<n;k++){
    int x, y; cin >> x >> y;
    tentative_BB.set(x, y);
  }

  // 木の配置を出力
  cout << (int)(add_list.size()/2);
  for (size_t i=0;i<add_list.size();i++){
    cout << ' ' << add_list[i];
  }
  cout << '\n' << flush;
  current_coord = {pi, pj};

  // 2 ターン目以降
  while (true){
    if (!(cin >> pi >> pj)) break;
    if (!(cin >> n)) break;
    for (int k=0;k<n;k++){
      int x, y; cin >> x >> y;
      tentative_BB.set(x, y);
    }
    if (pi == goal.first && pj == goal.second){
      break;
    }
    // 追加配置なし
    cout << 0 << '\n' << flush;
    current_coord = {pi, pj};
  }
  return 0;
}
