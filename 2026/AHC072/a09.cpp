#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <functional>
#include <iostream>
#include <queue>
#include <string>
#include <tuple>
#include <unordered_set>
#include <utility>
#include <vector>

using namespace std;

constexpr double TIME_LIMIT = 1.85;
constexpr int MAX_HEIGHT = 8;
constexpr int MAX_MOVES = 100000;
constexpr int MAX_CELLS = 400;
constexpr int CHECKPOINT_INTERVAL = 32;

// 下位ニブルから順に下から上の色+1を並べる。0は空の塔。
using Board = array<uint32_t, MAX_CELLS>;

struct Jump {
  uint16_t dst;
  uint8_t length;
  char direction;
};

struct Step {
  uint16_t src, dst;
  uint8_t k, length;
  char direction;
};

struct Transition {
  uint32_t src_stack, dst_stack;
  int delta, homed;
};

struct Node {
  // 親と変更後の2マスだけを持ち、展開時に盤面を復元する。
  int parent, score, remaining, checkpoint;
  uint64_t hash;
  uint32_t src_stack, dst_stack;
  Step step;
};

using QueueEntry = tuple<int, int, int, int>;  // distance, remaining, -moved, node id
using Layer = priority_queue<QueueEntry, vector<QueueEntry>, greater<QueueEntry>>;

uint64_t mix_cell(int cell, uint32_t stack) {
  if (stack == 0) return 0;
  uint64_t x = (uint64_t(cell) << 32) | stack;
  x += 0x9e3779b97f4a7c15ULL;
  x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
  x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
  return x ^ (x >> 31);
}

int height(uint32_t stack) {
  return stack == 0 ? 0 : (35 - __builtin_clz(stack)) / 4;
}

uint32_t low_mask(int k) {
  return k == 0 ? 0 : (uint32_t(1) << (4 * k)) - 1;
}

class Solver {
  int n = 0, colors = 0, size = 0, initial_remaining = 0;
  int initial_score = 0;
  Board initial{};
  array<int, MAX_CELLS> nest_color{};
  vector<int> nests;
  vector<vector<Jump>> jumps;
  vector<vector<int>> neighbors;
  vector<vector<int>> distances, toward;
  chrono::steady_clock::time_point start;

  double elapsed() const {
    return chrono::duration<double>(chrono::steady_clock::now() - start).count();
  }

  char direction_between(int src, int dst) const {
    if (src / n == dst / n) return src < dst ? 'R' : 'L';
    return src < dst ? 'D' : 'U';
  }

  Transition apply(const Board& board, int src, int dst, int k) const {
    uint32_t source = board[src];
    uint32_t target = board[dst];
    int h = height(source), g = height(target);
    int count = h - k;
    uint32_t moving = source >> (4 * k);
    uint32_t reversed = 0;
    int delta = 0;
    for (int i = 0; i < count; ++i) {
      int code = moving & 15;
      reversed = (reversed << 4) | code;
      delta += distances[code - 1][dst] - distances[code - 1][src];
      moving >>= 4;
    }
    uint32_t source_after = source & low_mask(k);
    uint32_t target_after = target | (reversed << (4 * g));
    int homed = 0;
    auto remove_home = [&](uint32_t& stack, int& stack_height, int home) {
      if (home < 0) return;
      while (stack_height > 0 &&
             int((stack >> (4 * (stack_height - 1))) & 15) == home + 1) {
        stack &= low_mask(stack_height - 1);
        --stack_height;
        ++homed;
      }
    };
    int target_height = g + count;
    remove_home(source_after, k, nest_color[src]);
    remove_home(target_after, target_height, nest_color[dst]);
    return {source_after, target_after, delta, homed};
  }

  uint64_t next_hash(uint64_t hash, const Board& board, int src, int dst,
                     const Transition& transition) const {
    return hash ^ mix_cell(src, board[src]) ^ mix_cell(dst, board[dst]) ^
           mix_cell(src, transition.src_stack) ^ mix_cell(dst, transition.dst_stack);
  }

  vector<Step> greedy(Board board, int& final_remaining) const {
    int remaining = initial_remaining;
    vector<Step> path;
    path.reserve(2000);
    while (remaining > 0 && int(path.size()) < MAX_MOVES) {
      if ((path.size() & 255) == 0 && elapsed() >= TIME_LIMIT) break;
      bool found = false;
      int best_delta = 0, best_homed = 0, best_count = 0;
      Step best_step{};
      Transition best_transition{};
      for (int src = 0; src < size; ++src) {
        int h = height(board[src]);
        if (h == 0) continue;
        for (const Jump& jump : jumps[src]) {
          int dst = jump.dst;
          int capacity = MAX_HEIGHT - height(board[dst]);
          if (capacity == 0) continue;
          int min_k = max({0, int(jump.length) - 1, h - capacity});
          for (int k = h - 1; k >= min_k; --k) {
            Transition t = apply(board, src, dst, k);
            int count = h - k;
            if (!found || make_tuple(t.delta, -t.homed, -count) <
                              make_tuple(best_delta, -best_homed, -best_count)) {
              found = true;
              best_delta = t.delta;
              best_homed = t.homed;
              best_count = count;
              best_step = {uint16_t(src), uint16_t(dst), uint8_t(k),
                           jump.length, jump.direction};
              best_transition = t;
            }
          }
        }
      }
      auto commit = [&](const Step& step, const Transition& t) {
        board[step.src] = t.src_stack;
        board[step.dst] = t.dst_stack;
        remaining -= t.homed;
        path.push_back(step);
      };
      if (found && (best_delta < 0 || best_homed > 0)) {
        commit(best_step, best_transition);
        continue;
      }

      // 08 と同じく、改善手が無いときは頂上の1匹を巣へ向けて運ぶ。
      vector<pair<int, int>> top_slimes;
      for (int src = 0; src < size; ++src) {
        int h = height(board[src]);
        if (h == 0) continue;
        int color = ((board[src] >> (4 * (h - 1))) & 15) - 1;
        top_slimes.push_back({distances[color][src], src});
      }
      sort(top_slimes.begin(), top_slimes.end());
      bool progressed = false;
      for (auto [unused_distance, src] : top_slimes) {
        int h = height(board[src]);
        int color = ((board[src] >> (4 * (h - 1))) & 15) - 1;
        while (src != nests[color] && int(path.size()) < MAX_MOVES) {
          int dst = toward[color][src];
          if (height(board[dst]) == MAX_HEIGHT) break;
          int k = height(board[src]) - 1;
          Step step{uint16_t(src), uint16_t(dst), uint8_t(k), 1,
                    direction_between(src, dst)};
          commit(step, apply(board, src, dst, k));
          src = dst;
          progressed = true;
        }
        if (progressed) break;
      }
      if (!progressed && found) commit(best_step, best_transition);
      if (!progressed && !found) break;
    }
    final_remaining = remaining;
    return path;
  }

  Board restore(int id, const vector<Node>& nodes,
                const vector<Board>& checkpoints) const {
    vector<int> chain;
    int cur = id;
    while (nodes[cur].checkpoint < 0) {
      chain.push_back(cur);
      cur = nodes[cur].parent;
    }
    Board board = checkpoints[nodes[cur].checkpoint];
    for (auto it = chain.rbegin(); it != chain.rend(); ++it) {
      const Node& node = nodes[*it];
      board[node.step.src] = node.src_stack;
      board[node.step.dst] = node.dst_stack;
    }
    return board;
  }

  vector<Step> restore_path(int id, const vector<Node>& nodes) const {
    vector<Step> path;
    while (nodes[id].parent >= 0) {
      path.push_back(nodes[id].step);
      id = nodes[id].parent;
    }
    reverse(path.begin(), path.end());
    return path;
  }

 public:
  void read() {
    cin >> n >> colors;
    size = n * n;
    vector<string> rows(n);
    for (string& row : rows) cin >> row;
    nests.assign(colors, -1);
    nest_color.fill(-1);
    vector<char> floor(size, false);
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < n; ++j) {
        int v = i * n + j;
        char cell = rows[i][j];
        if (cell == '#') continue;
        floor[v] = true;
        if ('a' <= cell && cell <= 'l') {
          initial[v] = uint32_t(cell - 'a' + 1);
          ++initial_remaining;
        } else if ('A' <= cell && cell <= 'L') {
          int color = cell - 'A';
          nests[color] = v;
          nest_color[v] = color;
        }
      }
    }
    jumps.resize(size);
    neighbors.resize(size);
    constexpr int di[4] = {-1, 1, 0, 0};
    constexpr int dj[4] = {0, 0, -1, 1};
    constexpr char directions[4] = {'U', 'D', 'L', 'R'};
    for (int src = 0; src < size; ++src) {
      if (!floor[src]) continue;
      int i = src / n, j = src % n;
      for (int direction = 0; direction < 4; ++direction) {
        for (int length = 1; length <= MAX_HEIGHT; ++length) {
          int ni = i + di[direction] * length;
          int nj = j + dj[direction] * length;
          if (ni < 0 || ni >= n || nj < 0 || nj >= n) break;
          int dst = ni * n + nj;
          if (!floor[dst]) break;
          jumps[src].push_back({uint16_t(dst), uint8_t(length),
                                directions[direction]});
          if (length == 1) neighbors[src].push_back(dst);
        }
      }
    }
    distances.resize(colors);
    toward.resize(colors);
    for (int color = 0; color < colors; ++color) {
      vector<int> dist(size, -1), parent(size, -1);
      queue<int> q;
      dist[nests[color]] = 0;
      q.push(nests[color]);
      while (!q.empty()) {
        int v = q.front();
        q.pop();
        for (int u : neighbors[v]) {
          if (dist[u] >= 0) continue;
          dist[u] = dist[v] + 1;
          parent[u] = v;
          q.push(u);
        }
      }
      distances[color] = move(dist);
      toward[color] = move(parent);
    }
    for (int v = 0; v < size; ++v) {
      if (initial[v]) {
        int color = (initial[v] & 15) - 1;
        initial_score += distances[color][v];
      }
    }
  }

  void solve() {
    start = chrono::steady_clock::now();
    int greedy_remaining;
    vector<Step> answer = greedy(initial, greedy_remaining);
    int best_turns = greedy_remaining == 0 ? int(answer.size()) : MAX_MOVES + 1;

    vector<Node> nodes;
    nodes.reserve(100000);
    vector<Board> checkpoints;
    checkpoints.push_back(initial);
    uint64_t root_hash = 0;
    for (int v = 0; v < size; ++v) root_hash ^= mix_cell(v, initial[v]);
    nodes.push_back({-1, initial_score, initial_remaining, 0,
                     root_hash, 0, 0, {0, 0, 0, 0, 'U'}});
    vector<Layer> layers(1);
    vector<unordered_set<uint64_t>> seen(1);
    layers[0].emplace(initial_score, initial_remaining, 0, 0);
    seen[0].insert(root_hash);

    bool timed_out = false;
    while (!timed_out && elapsed() < TIME_LIMIT) {
      bool expanded = false;
      bool restart = false;
      for (int depth = 0; depth < int(layers.size()); ++depth) {
        if (depth + 1 >= best_turns) break;
        if (elapsed() >= TIME_LIMIT) {
          timed_out = true;
          break;
        }
        if (layers[depth].empty()) continue;
        expanded = true;
        int id = get<3>(layers[depth].top());
        layers[depth].pop();
        Board board = restore(id, nodes, checkpoints);
        // 展開済みの節点を間隔ごとに保存し、復元時の親探索を短くする。
        if (depth % CHECKPOINT_INTERVAL == 0 && nodes[id].checkpoint < 0) {
          nodes[id].checkpoint = checkpoints.size();
          checkpoints.push_back(board);
        }
        Node parent = nodes[id];
        if (int(layers.size()) <= depth + 1) {
          layers.resize(depth + 2);
          seen.resize(depth + 2);
        }
        auto& next_layer = layers[depth + 1];
        auto& next_seen = seen[depth + 1];
        int checked = 0;
        for (int src = 0; src < size && !restart && !timed_out; ++src) {
          int h = height(board[src]);
          if (h == 0) continue;
          for (const Jump& jump : jumps[src]) {
            int dst = jump.dst;
            int capacity = MAX_HEIGHT - height(board[dst]);
            if (capacity == 0) continue;
            int min_k = max({0, int(jump.length) - 1, h - capacity});
            for (int k = h - 1; k >= min_k; --k) {
              if ((++checked & 1023) == 0 && elapsed() >= TIME_LIMIT) {
                timed_out = true;
                break;
              }
              Transition t = apply(board, src, dst, k);
              int child_remaining = parent.remaining - t.homed;
              if (depth + 1 >= best_turns) continue;
              uint64_t hash = next_hash(parent.hash, board, src, dst, t);
              if (!next_seen.insert(hash).second) continue;
              Step step{uint16_t(src), uint16_t(dst), uint8_t(k),
                        jump.length, jump.direction};
              int child_id = nodes.size();
              nodes.push_back({id, parent.score + t.delta,
                               child_remaining, -1, hash,
                               t.src_stack, t.dst_stack, step});
              if (child_remaining == 0) {
                best_turns = depth + 1;
                answer = restore_path(child_id, nodes);
                restart = true;
                break;
              }
              next_layer.emplace(parent.score + t.delta, child_remaining,
                                 -(h - k), child_id);
            }
            if (restart || timed_out) break;
          }
        }
        if (restart || timed_out) break;
      }
      // 手数の上限内で展開待ちの状態が無ければ、探索空間を使い切った。
      if (!expanded) break;
    }

    for (const Step& step : answer) {
      cout << step.src / n << ' ' << step.src % n << ' ' << int(step.k)
           << ' ' << step.direction << ' ' << int(step.length) << '\n';
    }
    cerr << "score: " << answer.size() << '\n';
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  Solver solver;
  solver.read();
  solver.solve();
}
