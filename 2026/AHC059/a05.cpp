#include <bits/stdc++.h>
using namespace std;

static constexpr int N = 20;
static constexpr double TIME_LIMIT = 1.9;
static constexpr int MAX_WIDTH = 1000;

struct Pos {
    int x, y;
};

static inline int manhattan(const Pos& a, const Pos& b) {
    return abs(a.x - b.x) + abs(a.y - b.y);
}

struct IsUsedBB {
    std::bitset<N * N> board;
    inline bool is_used(int x, int y) const { return board.test(x * N + y); }
    inline void set_used(int x, int y) { board.set(x * N + y); }
};

static inline Pos get_pair_pos(int num, const vector<array<Pos, 2>>& idx, const Pos& other) {
    const Pos& p1 = idx[num][0];
    const Pos& p2 = idx[num][1];
    if (p1.x == other.x && p1.y == other.y) return p2;
    return p1;
}

struct Node {
    IsUsedBB used;
    Pos current_pos{0, 0};
    bool has_stack_top = false;
    Pos stack_top{0, 0};

    int prev_path_length = 0;
    const Node* prev_node = nullptr;

    // Bounded container の lazy deletion 用
    bool alive = false;

    inline int total_cost() const {
        return has_stack_top ? (prev_path_length + manhattan(current_pos, stack_top)) : prev_path_length;
    }
};

// 幅制限付きの「best pop（min）」＋「worst drop（max）」両対応コンテナ
class BoundedBeam {
public:
    explicit BoundedBeam(int limit) : limit_(limit) {}

    bool empty() const { return alive_cnt_ == 0; }
    int alive_size() const { return alive_cnt_; }

    // いまの worst cost（alive がいなければ INF）
    int worst_cost() {
        clean_max();
        if (alive_cnt_ == 0) return INF;
        return maxpq_.top().cost;
    }

    // cost の候補が入る見込みがあるか（入らないならノード確保自体を避ける）
    bool would_accept(int cost) {
        clean_max();
        if (alive_cnt_ < limit_) return true;
        return cost < maxpq_.top().cost;
    }

    // ノードを追加（必要なら worst を落として幅を維持）
    void insert(Node* node) {
        node->alive = true;
        int cost = node->prev_path_length;
        minpq_.push({cost, node});
        maxpq_.push({cost, node});
        alive_cnt_++;

        if (alive_cnt_ > limit_) remove_worst();

        // lazy 削除のゴミが増えすぎると PQ 自体のメモリが増えるので適宜再構築
        maybe_rebuild();
    }

    // best（最小 cost）を取り出す（alive から外れる）
    Node* pop_best() {
        while (true) {
            clean_min();
            if (minpq_.empty()) return nullptr; // alive_cnt_==0 のはずだが保険
            auto e = minpq_.top(); minpq_.pop();
            if (!e.node->alive) continue; // stale
            e.node->alive = false;
            alive_cnt_--;
            return e.node;
        }
    }

    // コンテナ内の alive ノードを全て回収（探索終了後の最終選択用）
    vector<Node*> extract_all_alive() {
        vector<Node*> res;
        res.reserve(alive_cnt_);
        clean_min();
        while (!minpq_.empty()) {
            auto e = minpq_.top(); minpq_.pop();
            if (e.node->alive) {
                e.node->alive = false;
                res.push_back(e.node);
            }
        }
        // 状態クリア
        alive_cnt_ = 0;
        while (!maxpq_.empty()) maxpq_.pop();
        return res;
    }

private:
    static constexpr int INF = 1e9;

    struct Entry {
        int cost;
        Node* node;
    };
    struct MinCmp {
        bool operator()(const Entry& a, const Entry& b) const { return a.cost > b.cost; } // min-heap
    };
    struct MaxCmp {
        bool operator()(const Entry& a, const Entry& b) const { return a.cost < b.cost; } // max-heap
    };

    int limit_;
    int alive_cnt_ = 0;

    priority_queue<Entry, vector<Entry>, MinCmp> minpq_;
    priority_queue<Entry, vector<Entry>, MaxCmp> maxpq_;

    void clean_min() {
        while (!minpq_.empty() && !minpq_.top().node->alive) minpq_.pop();
    }
    void clean_max() {
        while (!maxpq_.empty() && !maxpq_.top().node->alive) maxpq_.pop();
    }

    void remove_worst() {
        while (true) {
            clean_max();
            if (maxpq_.empty()) return; // 保険
            auto e = maxpq_.top(); maxpq_.pop();
            if (!e.node->alive) continue;
            e.node->alive = false;
            alive_cnt_--;
            return;
        }
    }

    void maybe_rebuild() {
        // stale が多いと PQ が膨らむので、サイズが上限の数倍になったら掃除
        // （閾値は適当。必要に応じて調整可能）
        if ((int)minpq_.size() <= 6 * max(1, alive_cnt_) &&
            (int)maxpq_.size() <= 6 * max(1, alive_cnt_)) return;

        // minpq から alive を集めて再構築
        vector<Node*> alive_nodes;
        alive_nodes.reserve(alive_cnt_);

        clean_min();
        while (!minpq_.empty()) {
            auto e = minpq_.top(); minpq_.pop();
            if (e.node->alive) alive_nodes.push_back(e.node);
        }
        while (!maxpq_.empty()) maxpq_.pop();

        // 再投入
        for (Node* nd : alive_nodes) {
            int cost = nd->prev_path_length;
            minpq_.push({cost, nd});
            maxpq_.push({cost, nd});
        }
        // alive_cnt_ は変化なし
    }
};

static vector<char> make_commands(const vector<Pos>& collect_order, Pos current_pos) {
    vector<char> commands;
    int x = current_pos.x, y = current_pos.y;

    for (const auto& target : collect_order) {
        int tx = target.x, ty = target.y;

        while (x < tx) { commands.push_back('D'); x++; }
        while (x > tx) { commands.push_back('U'); x--; }
        while (y < ty) { commands.push_back('R'); y++; }
        while (y > ty) { commands.push_back('L'); y--; }

        commands.push_back('Z');
    }
    return commands;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int Nin;
    cin >> Nin; // 固定なので無視

    vector<vector<int>> grid(N, vector<int>(N));
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) cin >> grid[i][j];
    }

    const int M = (N * N) / 2; // 200
    vector<array<Pos, 2>> nums_idx_list(M);
    vector<int> cnt(M, 0);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            int num = grid[i][j];
            int k = cnt[num]++;
            nums_idx_list[num][k] = Pos{i, j};
        }
    }

    // ノードは採用されたものだけ確保する（ここがメモリ対策の要点）
    deque<Node> pool;

    pool.emplace_back();
    Node* root = &pool.back();
    root->used = IsUsedBB{};
    root->current_pos = Pos{0, 0};
    root->has_stack_top = false;
    root->prev_path_length = 0;
    root->prev_node = nullptr;

    const int LEVELS = M + 1; // 201
    vector<BoundedBeam> levels;
    levels.reserve(LEVELS);
    for (int i = 0; i < LEVELS; i++) levels.emplace_back(MAX_WIDTH);

    levels[0].insert(root);

    auto start = chrono::steady_clock::now();
    bool flag = true;

    while (flag) {
        for (int lv = 0; lv < M; lv++) {
            if (levels[lv].empty()) continue;

            Node* node = levels[lv].pop_best();
            if (!node) continue;

            // node から lv+1 を生成
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    if (node->used.is_used(i, j)) continue;

                    Pos cand{i, j};
                    int num = grid[i][j];
                    Pos pair_pos = get_pair_pos(num, nums_idx_list, cand);

                    int dist1 = manhattan(node->current_pos, cand);
                    int dist2 = node->has_stack_top ? manhattan(node->stack_top, pair_pos) : 0;
                    int new_cost = node->prev_path_length + dist1 + dist2;

                    // ここで「入らない候補は確保しない」ことでメモリを劇的に削減
                    if (!levels[lv + 1].would_accept(new_cost)) continue;

                    pool.emplace_back();
                    Node* nn = &pool.back();
                    nn->used = node->used;
                    nn->used.set_used(i, j);
                    nn->used.set_used(pair_pos.x, pair_pos.y);

                    nn->current_pos = cand;
                    nn->has_stack_top = true;
                    nn->stack_top = pair_pos;
                    nn->prev_path_length = new_cost;
                    nn->prev_node = node;

                    levels[lv + 1].insert(nn);
                }
            }

            double elapsed = chrono::duration<double>(chrono::steady_clock::now() - start).count();
            if (elapsed > TIME_LIMIT) { flag = false; break; }
        }
    }

    // Python版は最終レベルで total_cost 最小を選ぶ。
    // ただしタイムアウトで最終レベルが空の可能性があるので、最深の非空レベルから選ぶ。
    Node* best_node = root;
    for (int lv = LEVELS - 1; lv >= 0; lv--) {
        if (!levels[lv].empty()) {
            auto nodes = levels[lv].extract_all_alive();
            best_node = nodes[0];
            for (Node* nd : nodes) {
                if (nd->total_cost() < best_node->total_cost()) best_node = nd;
            }
            break;
        }
    }

    // 経路再構築（Python版の挙動を踏襲：後半 path_2 は reverse しない）
    vector<Pos> path;
    vector<Pos> path_2;
    const Node* cur = best_node;
    while (cur != nullptr) {
        path.push_back(cur->current_pos);
        if (cur->has_stack_top) path_2.push_back(cur->stack_top);
        cur = cur->prev_node;
    }
    if (!path.empty()) path.pop_back(); // (0,0) 期待
    reverse(path.begin(), path.end());
    path.insert(path.end(), path_2.begin(), path_2.end());

    auto commands = make_commands(path, Pos{0, 0});
    for (char c : commands) cout << c << "\n";

    return 0;
}
