#include <bits/stdc++.h>
using namespace std;

static constexpr int N = 20;   // 固定
static constexpr int K = 50;   // ビーム幅

struct Pos {
    int x, y;
    bool operator==(const Pos& other) const { return x == other.x && y == other.y; }
};

inline int manhattan_dist(const Pos& a, const Pos& b) {
    return abs(a.x - b.x) + abs(a.y - b.y);
}

inline bool is_valid_pos(int x, int y) {
    return 0 <= x && x < N && 0 <= y && y < N;
}

// 20x20 = 400 bit を uint64_t で保持（7 * 64 = 448 bit）
struct IsUsedBB {
    array<uint64_t, 7> b{};

    bool is_used(int x, int y) const {
        int idx = x * N + y;
        int w = idx >> 6;
        int r = idx & 63;
        return (b[w] >> r) & 1ULL;
    }

    void set_used(int x, int y) {
        int idx = x * N + y;
        int w = idx >> 6;
        int r = idx & 63;
        b[w] |= (1ULL << r);
    }
};

// Python 側にあった「最寄り未使用マス探索」：本コードでは未使用（移植のみ）
Pos nearest_valid(const Pos& start, const IsUsedBB& used) {
    deque<tuple<int,int,int>> q;
    vector<vector<bool>> vis(N, vector<bool>(N, false));
    q.emplace_back(start.x, start.y, 0);
    vis[start.x][start.y] = true;

    static const int dx[4] = {1,-1,0,0};
    static const int dy[4] = {0,0,1,-1};

    while (!q.empty()) {
        auto [cx, cy, d] = q.front();
        q.pop_front();

        if (!used.is_used(cx, cy)) return Pos{cx, cy};

        for (int dir = 0; dir < 4; dir++) {
            int nx = cx + dx[dir], ny = cy + dy[dir];
            if (is_valid_pos(nx, ny) && !vis[nx][ny]) {
                vis[nx][ny] = true;
                q.emplace_back(nx, ny, d + 1);
            }
        }
    }
    throw runtime_error("No unused cell found");
}

Pos get_pair_pos(int num, const vector<vector<Pos>>& nums_idx_list, const Pos& known_pos) {
    // nums_idx_list[num] は必ず2要素ある前提（問題設定）
    const Pos& p1 = nums_idx_list[num][0];
    const Pos& p2 = nums_idx_list[num][1];
    return (p1 == known_pos) ? p2 : p1;
}

vector<char> make_commands(const vector<Pos>& collect_order, const Pos& start_pos) {
    vector<char> commands;
    int x = start_pos.x, y = start_pos.y;

    for (const auto& target : collect_order) {
        int tx = target.x, ty = target.y;

        while (x < tx) { commands.push_back('D'); x++; }
        while (x > tx) { commands.push_back('U'); x--; }
        while (y < ty) { commands.push_back('R'); y++; }
        while (y > ty) { commands.push_back('L'); y--; }

        commands.push_back('Z'); // 取る
        x = tx; y = ty;
    }
    return commands;
}

long long get_path_length(const vector<Pos>& path) {
    long long length = 0;
    for (size_t i = 1; i < path.size(); i++) {
        length += manhattan_dist(path[i-1], path[i]);
    }
    return length;
}

// ビームサーチ用ノード
struct Node : enable_shared_from_this<Node> {
    IsUsedBB used;
    Pos current_pos;
    optional<Pos> stack_top; // Python の None 相当
    int prev_path_length = 0;
    shared_ptr<Node> prev_node;

    Node(const IsUsedBB& used_,
         const Pos& current_pos_,
         optional<Pos> stack_top_ = nullopt,
         int prev_path_length_ = 0,
         shared_ptr<Node> prev_node_ = nullptr)
        : used(used_),
          current_pos(current_pos_),
          stack_top(stack_top_),
          prev_path_length(prev_path_length_),
          prev_node(std::move(prev_node_)) {}

    vector<shared_ptr<Node>> next_nodes(const vector<vector<int>>& grid,
                                        const vector<vector<Pos>>& nums_idx_list) {
        vector<shared_ptr<Node>> res;
        res.reserve(N * N);

        auto self = shared_from_this();
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (used.is_used(i, j)) continue;

                Pos candidate{i, j};
                int num = grid[i][j];
                Pos pair_pos = get_pair_pos(num, nums_idx_list, candidate);

                IsUsedBB new_used = used;
                new_used.set_used(i, j);
                new_used.set_used(pair_pos.x, pair_pos.y);

                int dist_1 = manhattan_dist(current_pos, candidate);
                int dist_2 = stack_top.has_value() ? manhattan_dist(*stack_top, pair_pos) : 0;

                int new_path_length = prev_path_length + dist_1 + dist_2;

                res.emplace_back(make_shared<Node>(
                    new_used,
                    candidate,
                    pair_pos,
                    new_path_length,
                    self
                ));
            }
        }
        return res;
    }

    vector<Pos> reconstruct_path() const {
        vector<Pos> path;
        vector<Pos> path_2;

        const Node* node = this;
        // shared_ptr を辿る必要があるため、一旦 shared_ptr を使って辿る
        // ただし this は生ポインタなので、外側で shared_ptr を使う設計に合わせて実装する
        // ここでは prev_node を辿るために shared_ptr を使う
        shared_ptr<const Node> cur = nullptr;

        // this を shared_ptr で参照できないので、呼び出し側が shared_ptr<Node> で保持している前提で
        // 本関数は best_node->reconstruct_path() 形式で呼ばれる（best_node は shared_ptr）
        // よって、実装を別に用意するのが安全だが、簡潔化のため呼び出し側で shared_ptr 版を使う。
        throw runtime_error("reconstruct_path() should be called via reconstruct_path_from_shared().");
    }

    vector<Pos> reconstruct_path_from_shared(shared_ptr<Node> self) {
        vector<Pos> path;
        vector<Pos> path_2;

        shared_ptr<Node> node = std::move(self);
        while (node) {
            path.push_back(node->current_pos);
            if (node->stack_top.has_value()) path_2.push_back(*node->stack_top);
            node = node->prev_node;
        }

        // root の (0,0) は重複しているので削除（Python と同じ）
        Pos first = path.back();
        path.pop_back();
        if (!(first == Pos{0,0})) {
            throw runtime_error("The first position is not (0,0)");
        }

        reverse(path.begin(), path.end());
        // path_2 は leaf→root の順で積まれている（LIFO で回収する想定）のでそのまま append（Python と同じ）
        path.insert(path.end(), path_2.begin(), path_2.end());
        return path;
    }

    int total_cost() const {
        if (stack_top.has_value()) {
            return prev_path_length + manhattan_dist(current_pos, *stack_top);
        }
        return prev_path_length;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int Nin;
    cin >> Nin; // N=20固定なので無視

    vector<vector<int>> grid(N, vector<int>(N));
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) cin >> grid[i][j];
    }

    // Python と同様に N^2 サイズを確保（実際に使う番号は 0..N^2/2-1）
    vector<vector<Pos>> nums_idx_list(N * N);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            int num = grid[i][j];
            nums_idx_list[num].push_back(Pos{i, j});
        }
    }

    IsUsedBB used;
    Pos start{0, 0};

    auto root = make_shared<Node>(used, start, nullopt, 0, nullptr);
    vector<shared_ptr<Node>> beam_nodes{root};

    for (int step = 0; step < (N * N / 2); step++) {
        vector<shared_ptr<Node>> next_beam_nodes;
        // 大雑把な予約（過小でもOK）
        next_beam_nodes.reserve(beam_nodes.size() * (N * N - 2 * step));

        for (auto& node : beam_nodes) {
            auto nxt = node->next_nodes(grid, nums_idx_list);
            next_beam_nodes.insert(next_beam_nodes.end(),
                                   make_move_iterator(nxt.begin()),
                                   make_move_iterator(nxt.end()));
        }

        if (step < (N * N / 2 - 1)) {
            sort(next_beam_nodes.begin(), next_beam_nodes.end(),
                 [](const shared_ptr<Node>& a, const shared_ptr<Node>& b) {
                     return a->prev_path_length < b->prev_path_length;
                 });
        } else {
            sort(next_beam_nodes.begin(), next_beam_nodes.end(),
                 [](const shared_ptr<Node>& a, const shared_ptr<Node>& b) {
                     return a->total_cost() < b->total_cost();
                 });
        }

        if ((int)next_beam_nodes.size() > K) next_beam_nodes.resize(K);
        beam_nodes = std::move(next_beam_nodes);
    }

    auto best_node = beam_nodes[0];
    vector<Pos> collect_order = best_node->reconstruct_path_from_shared(best_node);

    vector<char> commands = make_commands(collect_order, start);
    for (char c : commands) {
        cout << c << "\n";
    }

    long long total_length = get_path_length(collect_order);
    cerr << "Total path length: " << total_length << "\n";

    return 0;
}
