#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <deque>
#include <iostream>
#include <optional>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
using namespace std;

constexpr int MAX_HEIGHT = 7;
constexpr int MAX_TREE_SLIMES = 7;
constexpr int BEAM_WIDTH = 1000;
constexpr int BEAM_DEPTH_LIMIT = 90;
constexpr uint16_t EMPTY_GROUP = 65535;

struct Step {
  int src, dst, count;
};

struct OutputStep {
  int i, j, k, length;
  char direction;
};

struct Search {
  vector<int> distance, next;
};

struct Tree {
  vector<int> parent;
  vector<int> order;
};

// One group uses 9 bits for its cell, 3 for its size, and 1 for its lock.
using State = array<uint16_t, MAX_TREE_SLIMES>;

uint16_t encode_group(int pos, int count, bool locked) {
  return static_cast<uint16_t>((pos << 4) | (count << 1) | int(locked));
}

int group_pos(uint16_t group) { return group >> 4; }
int group_count(uint16_t group) { return (group >> 1) & 7; }
bool group_locked(uint16_t group) { return group & 1; }

struct StateHash {
  size_t operator()(const State& state) const {
    uint64_t hash = 1469598103934665603ULL;
    for (uint16_t group : state) {
      hash ^= group;
      hash *= 1099511628211ULL;
    }
    return static_cast<size_t>(hash);
  }
};

struct Node {
  State state;
  int score, weighted, parent;
  Step action;
};

struct Candidate {
  State state;
  int score, count, weighted, parent;
  Step action;
};

bool better_candidate(const Candidate& a, const Candidate& b) {
  if (a.score != b.score) return a.score < b.score;
  if (a.count != b.count) return a.count < b.count;
  if (a.weighted != b.weighted) return a.weighted < b.weighted;
  return a.state < b.state;
}

class Solver {
 public:
  int n, k, size, remaining = 0;
  vector<vector<int>> towers;
  vector<int> nests;
  vector<char> floor;
  vector<vector<pair<int, char>>> neighbors;
  vector<vector<pair<int, int>>> outgoing, incoming;
  vector<vector<int>> dist_to_nest, toward_nest;
  vector<OutputStep> answer;

  void read() {
    cin >> n >> k;
    size = n * n;
    towers.resize(size);
    nests.assign(k, -1);
    floor.assign(size, false);
    vector<string> board(n);
    for (auto& row : board) cin >> row;
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < n; ++j) {
        int v = i * n + j;
        char cell = board[i][j];
        if (cell == '#') continue;
        floor[v] = true;
        if ('a' <= cell && cell <= 'l') {
          towers[v].push_back(cell - 'a');
          ++remaining;
        } else if ('A' <= cell && cell <= 'L') {
          nests[cell - 'A'] = v;
        }
      }
    }

    neighbors.resize(size);
    outgoing.resize(size);
    incoming.resize(size);
    constexpr int di[4] = {-1, 1, 0, 0};
    constexpr int dj[4] = {0, 0, -1, 1};
    constexpr char directions[4] = {'U', 'D', 'L', 'R'};
    for (int v = 0; v < size; ++v) {
      if (!floor[v]) continue;
      int i = v / n, j = v % n;
      for (int d = 0; d < 4; ++d) {
        for (int length = 1; length <= MAX_HEIGHT + 1; ++length) {
          int ni = i + di[d] * length, nj = j + dj[d] * length;
          if (ni < 0 || ni >= n || nj < 0 || nj >= n) break;
          int u = ni * n + nj;
          if (!floor[u]) break;
          outgoing[v].push_back({u, length});
          incoming[u].push_back({v, length});
          if (length == 1) neighbors[v].push_back({u, directions[d]});
        }
      }
    }

    dist_to_nest.resize(k);
    toward_nest.resize(k);
    for (int color = 0; color < k; ++color) {
      vector<int> dist(size, -1), toward(size, -1);
      int root = nests[color];
      dist[root] = 0;
      queue<int> q;
      q.push(root);
      while (!q.empty()) {
        int v = q.front(); q.pop();
        for (auto [u, direction] : neighbors[v]) {
          if (dist[u] >= 0) continue;
          dist[u] = dist[v] + 1;
          toward[u] = v;
          q.push(u);
        }
      }
      dist_to_nest[color] = move(dist);
      toward_nest[color] = move(toward);
    }
  }

  Search jump_search(const vector<int>& targets, int color,
                     const vector<char>& used) const {
    vector<int> reach(size);
    for (int v = 0; v < size; ++v) {
      int count = 0;
      if (used[v]) {
        for (int slime : towers[v]) count += slime == color;
      }
      reach[v] = min(MAX_HEIGHT, 1 + int(towers[v].size()) - count);
    }
    Search result{vector<int>(size, -1), vector<int>(size, -1)};
    queue<int> q;
    for (int v : targets) {
      result.distance[v] = 0;
      q.push(v);
    }
    while (!q.empty()) {
      int v = q.front(); q.pop();
      for (auto [u, length] : incoming[v]) {
        if (result.distance[u] >= 0 || length > reach[u]) continue;
        result.distance[u] = result.distance[v] + 1;
        result.next[u] = v;
        q.push(u);
      }
    }
    return result;
  }

  pair<int, int> start_step(int v, const Search& search) const {
    if (search.distance[v] == 0) return {0, v};
    pair<int, int> best = {size + 1, -1};
    for (auto [u, length] : outgoing[v]) {
      if (length > int(towers[v].size()) || search.distance[u] < 0) continue;
      pair<int, int> candidate = {search.distance[u] + 1, u};
      if (candidate >= best) continue;
      int cur = u;
      while (cur != v && search.next[cur] >= 0) cur = search.next[cur];
      if (cur == v) continue;
      best = candidate;
    }
    return best;
  }

  pair<char, int> direction_and_length(int src, int dst) const {
    int si = src / n, sj = src % n, ti = dst / n, tj = dst % n;
    if (si == ti) return tj > sj ? make_pair('R', tj - sj) : make_pair('L', sj - tj);
    return ti > si ? make_pair('D', ti - si) : make_pair('U', si - ti);
  }

  void move_slimes(int src, int dst, int count) {
    int height = towers[src].size();
    int remain_here = height - count;
    auto [direction, length] = direction_and_length(src, dst);
    assert(0 <= remain_here && remain_here < height);
    assert(1 <= length && length <= remain_here + 1);
    assert(int(towers[dst].size()) + count <= MAX_HEIGHT);
    answer.push_back({src / n, src % n, remain_here, length, direction});
    for (int index = height - 1; index >= remain_here; --index) {
      towers[dst].push_back(towers[src][index]);
    }
    towers[src].resize(remain_here);
    for (int v : {src, dst}) {
      for (int color = 0; color < k; ++color) {
        if (v != nests[color]) continue;
        while (!towers[v].empty() && towers[v].back() == color) {
          towers[v].pop_back();
          --remaining;
        }
        break;
      }
    }
  }

  void make_room(int v, int avoid = -1) {
    if (int(towers[v].size()) < MAX_HEIGHT) return;
    int hole = -1;
    vector<int> previous;
    for (int excluded : {avoid, -1}) {
      previous.assign(size, -1);
      previous[v] = v;
      if (excluded >= 0 && excluded != v) previous[excluded] = excluded;
      queue<int> q;
      q.push(v);
      while (!q.empty() && hole < 0) {
        int cur = q.front(); q.pop();
        for (auto [nxt, direction] : neighbors[cur]) {
          if (previous[nxt] >= 0) continue;
          previous[nxt] = cur;
          if (int(towers[nxt].size()) < MAX_HEIGHT) {
            hole = nxt;
            break;
          }
          q.push(nxt);
        }
      }
      if (hole >= 0) break;
    }
    if (hole < 0) throw runtime_error("No room on the board");
    vector<int> path{hole};
    while (path.back() != v) path.push_back(previous[path.back()]);
    reverse(path.begin(), path.end());
    for (int index = int(path.size()) - 2; index >= 0; --index) {
      move_slimes(path[index], path[index + 1], 1);
    }
  }

  optional<Tree> build_tree(int color, int seed) const {
    int root = nests[color];
    Tree tree{vector<int>(size, -1), {root}};
    tree.parent[root] = root;
    vector<char> unused(size, false);
    Search nest_search = jump_search({root}, color, unused);
    int v = seed;
    int first = start_step(seed, nest_search).second;
    int slime_count = 0;
    while (v != root) {
      int nxt = first < 0 ? toward_nest[color][v]
                          : (v == seed ? first : nest_search.next[v]);
      tree.parent[v] = nxt;
      tree.order.push_back(v);
      for (int slime : towers[v]) slime_count += slime == color;
      if (slime_count > MAX_TREE_SLIMES) return nullopt;
      v = nxt;
    }
    if (slime_count == MAX_TREE_SLIMES) return tree;

    vector<int> positions;
    for (int pos = 0; pos < size; ++pos) {
      if (find(towers[pos].begin(), towers[pos].end(), color) != towers[pos].end()) {
        positions.push_back(pos);
      }
    }
    while (true) {
      vector<char> used(size, false);
      for (int pos : tree.order) used[pos] = true;
      Search search = jump_search(tree.order, color, used);
      int best_steps = size + 1, best_pos = -1, best_added = 0;
      vector<pair<int, int>> best_branch;
      for (int pos : positions) {
        if (tree.parent[pos] >= 0) continue;
        auto [to_tree, first_step] = start_step(pos, search);
        auto [to_nest, ignored] = start_step(pos, nest_search);
        if (to_tree >= to_nest || make_pair(to_tree, pos) >= make_pair(best_steps, best_pos)) {
          continue;
        }
        vector<pair<int, int>> branch;
        int u = pos;
        while (tree.parent[u] < 0) {
          int nxt = u == pos ? first_step : search.next[u];
          branch.push_back({u, nxt});
          u = nxt;
        }
        int added = 0;
        for (auto [cell, nxt] : branch) {
          for (int slime : towers[cell]) added += slime == color;
        }
        if (slime_count + added <= MAX_TREE_SLIMES) {
          best_steps = to_tree;
          best_pos = pos;
          best_branch = move(branch);
          best_added = added;
        }
      }
      if (best_pos < 0) break;
      for (auto [u, nxt] : best_branch) {
        tree.parent[u] = nxt;
        tree.order.push_back(u);
      }
      slime_count += best_added;
      if (slime_count == MAX_TREE_SLIMES) break;
    }
    return tree;
  }

  optional<vector<Step>> beam_route(int color, const Tree& tree) const {
    int root = nests[color];
    vector<int> selected(size, 0), base(size);
    for (int v : tree.order) {
      if (v == root) continue;
      for (auto it = towers[v].rbegin(); it != towers[v].rend() && *it == color; ++it) {
        ++selected[v];
      }
    }
    int selected_total = 0;
    for (int v = 0; v < size; ++v) {
      base[v] = int(towers[v].size()) - selected[v];
      selected_total += selected[v];
    }
    if (!selected_total) return nullopt;

    vector<int> distance(size, -1);
    distance[root] = 0;
    queue<int> q;
    q.push(root);
    while (!q.empty()) {
      int v = q.front(); q.pop();
      for (auto [u, length] : incoming[v]) {
        if (distance[u] >= 0 || length > base[u] + 1) continue;
        distance[u] = distance[v] + 1;
        q.push(u);
      }
    }

    State initial;
    initial.fill(EMPTY_GROUP);
    int initial_count = 0, score = 0, weighted = 0;
    for (int v = 0; v < size; ++v) {
      if (!selected[v]) continue;
      initial[initial_count++] = encode_group(v, selected[v], selected[v] > 1);
      score += distance[v];
      weighted += distance[v] * selected[v];
    }
    vector<Node> nodes{{initial, score, weighted, -1, {-1, -1, 0}}};
    vector<int> frontier{0};
    unordered_set<State, StateHash> seen;
    seen.insert(initial);
    int depth_limit = min(BEAM_DEPTH_LIMIT, max(24, 2 * weighted + 12));

    for (int depth = 0; depth < depth_limit; ++depth) {
      unordered_map<State, Candidate, StateHash> pool;
      for (int parent_id : frontier) {
        const Node& node = nodes[parent_id];
        for (int i = 0; i < MAX_TREE_SLIMES && node.state[i] != EMPTY_GROUP; ++i) {
          int src = group_pos(node.state[i]);
          int count_here = group_count(node.state[i]);
          bool locked = group_locked(node.state[i]);
          for (int moving = locked ? count_here : 1; moving <= count_here; ++moving) {
            int reach = base[src] + count_here - moving + 1;
            vector<uint16_t> without;
            for (int index = 0; index < MAX_TREE_SLIMES && node.state[index] != EMPTY_GROUP; ++index) {
              if (index != i) without.push_back(node.state[index]);
            }
            if (moving < count_here) {
              without.push_back(encode_group(src, count_here - moving, false));
            }
            for (auto [dst, length] : outgoing[src]) {
              if (length > reach) continue;
              int at_dst = 0;
              for (uint16_t group : node.state) {
                if (group == EMPTY_GROUP) break;
                if (group_pos(group) == dst) {
                  at_dst = group_count(group);
                  break;
                }
              }
              if (base[dst] + at_dst + moving > MAX_HEIGHT) continue;
              vector<uint16_t> groups = without;
              if (dst != root) {
                if (at_dst) {
                  groups.erase(remove_if(groups.begin(), groups.end(),
                                         [dst](uint16_t group) { return group_pos(group) == dst; }),
                               groups.end());
                  groups.push_back(encode_group(dst, at_dst + moving, true));
                } else {
                  groups.push_back(encode_group(dst, moving, locked));
                }
              }
              sort(groups.begin(), groups.end());
              State next;
              next.fill(EMPTY_GROUP);
              for (int index = 0; index < int(groups.size()); ++index) next[index] = groups[index];
              if (seen.find(next) != seen.end() || pool.find(next) != pool.end()) continue;
              Step action{src, dst, moving};
              if (groups.empty()) {
                vector<Step> route{action};
                int node_id = parent_id;
                while (node_id > 0) {
                  route.push_back(nodes[node_id].action);
                  node_id = nodes[node_id].parent;
                }
                reverse(route.begin(), route.end());
                return route;
              }
              int new_score = node.score - (moving == count_here ? distance[src] : 0);
              if (dst != root && !at_dst) new_score += distance[dst];
              int new_weighted = node.weighted - moving * distance[src];
              if (dst != root) new_weighted += moving * distance[dst];
              pool.emplace(next, Candidate{next, new_score, int(groups.size()),
                                           new_weighted, parent_id, action});
            }
          }
        }
      }
      if (pool.empty()) break;
      vector<Candidate> candidates;
      candidates.reserve(pool.size());
      for (auto& [key, value] : pool) candidates.push_back(value);
      int keep = min(BEAM_WIDTH, int(candidates.size()));
      partial_sort(candidates.begin(), candidates.begin() + keep, candidates.end(), better_candidate);
      frontier.clear();
      for (int index = 0; index < keep; ++index) {
        const Candidate& candidate = candidates[index];
        seen.insert(candidate.state);
        nodes.push_back({candidate.state, candidate.score, candidate.weighted,
                         candidate.parent, candidate.action});
        frontier.push_back(int(nodes.size()) - 1);
      }
    }
    return nullopt;
  }

  vector<int> shortest_single_path(int start, int goal) const {
    vector<int> previous(size, -1);
    previous[start] = start;
    queue<int> q;
    q.push(start);
    while (!q.empty() && previous[goal] < 0) {
      int v = q.front(); q.pop();
      int reach = int(towers[v].size()) + (v != start);
      for (auto [u, length] : outgoing[v]) {
        if (length > reach || int(towers[u].size()) >= MAX_HEIGHT || previous[u] >= 0) continue;
        previous[u] = v;
        q.push(u);
      }
    }
    if (previous[goal] < 0) return {};
    vector<int> path{goal};
    while (path.back() != start) path.push_back(previous[path.back()]);
    reverse(path.begin(), path.end());
    return path;
  }

  void return_one(int preferred = -1) {
    while (true) {
      int start = -1;
      if (preferred >= 0 && !towers[preferred].empty()) {
        start = preferred;
      } else {
        int best_distance = -1;
        for (int v = 0; v < size; ++v) {
          if (towers[v].empty()) continue;
          int distance = dist_to_nest[towers[v].back()][v];
          if (distance > best_distance) {
            best_distance = distance;
            start = v;
          }
        }
      }
      int color = towers[start].back(), goal = nests[color];
      vector<int> path = shortest_single_path(start, goal);
      if (path.empty()) {
        int v = start;
        while (toward_nest[color][v] != -1) {
          v = toward_nest[color][v];
          if (int(towers[v].size()) == MAX_HEIGHT) {
            make_room(v, start);
            break;
          }
        }
        continue;
      }
      for (int index = 0; index + 1 < int(path.size()); ++index) {
        move_slimes(path[index], path[index + 1], 1);
      }
      return;
    }
  }

  void send_on_tree(int v, int color, const Tree& tree) {
    if (v == nests[color]) return;
    int dst = tree.parent[v];
    while (!towers[v].empty() && towers[v].back() == color) {
      int height = towers[v].size();
      int run = 1;
      while (run < height && towers[v][height - run - 1] == color) ++run;
      int length = direction_and_length(v, dst).second;
      if (height - length + 1 <= 0) {
        vector<int> path = shortest_single_path(v, nests[color]);
        if (path.empty()) return_one(v);
        else {
          for (int index = 0; index + 1 < int(path.size()); ++index) {
            move_slimes(path[index], path[index + 1], 1);
          }
        }
        continue;
      }
      if (int(towers[dst].size()) == MAX_HEIGHT) {
        make_room(dst, v);
        continue;
      }
      int count = min({run, MAX_HEIGHT - int(towers[dst].size()), height - length + 1});
      move_slimes(v, dst, count);
    }
  }

  void solve() {
    while (remaining) {
      int seed = -1, color = -1;
      pair<int, bool> best = {size + 1, true};
      vector<char> unused(size, false);
      for (int c = 0; c < k; ++c) {
        Search search = jump_search({nests[c]}, c, unused);
        for (int v = 0; v < size; ++v) {
          if (find(towers[v].begin(), towers[v].end(), c) == towers[v].end()) continue;
          auto [steps, first] = start_step(v, search);
          pair<int, bool> candidate = {steps, towers[v].back() != c};
          if (candidate < best) {
            best = candidate;
            seed = v;
            color = c;
          }
        }
      }
      if (towers[seed].back() != color) {
        return_one(seed);
        continue;
      }
      int before = remaining;
      optional<Tree> tree = build_tree(color, seed);
      if (!tree) {
        return_one(seed);
        continue;
      }
      optional<vector<Step>> route = beam_route(color, *tree);
      if (route) {
        for (Step step : *route) move_slimes(step.src, step.dst, step.count);
      } else {
        vector<int> depth(size, -1);
        depth[nests[color]] = 0;
        for (int v : tree->order) {
          if (depth[v] >= 0) continue;
          vector<int> chain;
          int u = v;
          while (depth[u] < 0) {
            chain.push_back(u);
            u = tree->parent[u];
          }
          for (auto it = chain.rbegin(); it != chain.rend(); ++it) {
            depth[*it] = depth[tree->parent[*it]] + 1;
          }
        }
        vector<int> order = tree->order;
        stable_sort(order.begin(), order.end(), [&](int a, int b) { return depth[a] > depth[b]; });
        for (int v : order) send_on_tree(v, color, *tree);
      }
      if (remaining == before) return_one(seed);
    }
    for (const auto& step : answer) {
      cout << step.i << ' ' << step.j << ' ' << step.k << ' ' << step.direction
           << ' ' << step.length << '\n';
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
