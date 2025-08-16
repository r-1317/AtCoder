#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int,int>;

static const pii INLET = {0, 5000};
static const double TIME_LIMIT = 1.8;  // 秒
static const int X07 = 4;              // 完全二分木の高さ（元コードの定数）
static std::mt19937 rng(1317);

int sgn(long long x){ return (x>0)-(x<0); }

int orientation(const pii& a, const pii& b, const pii& c){
    long long cross = 1LL*(b.first-a.first)*(c.second-a.second) - 1LL*(b.second-a.second)*(c.first-a.first);
    return sgn(cross);
}

// 端点共有を交差とみなさない（inclusive 判定）版
bool segments_intersect_inclusive(const pii& p1, const pii& p2, const pii& q1, const pii& q2){
    if (max(p1.first, p2.first) < min(q1.first, q2.first) ||
        max(q1.first, q2.first) < min(p1.first, p2.first) ||
        max(p1.second, p2.second) < min(q1.second, q2.second) ||
        max(q1.second, q2.second) < min(p1.second, p2.second)) return false;
    int o1 = orientation(p1, p2, q1);
    int o2 = orientation(p1, p2, q2);
    int o3 = orientation(q1, q2, p1);
    int o4 = orientation(q1, q2, p2);
    return (1LL*o1*o2 <= 0) && (1LL*o3*o4 <= 0);
}

// スコア計算
long long calc_score(
    int N, int M, int K,
    const vector<vector<int>>& graph,
    const vector<vector<double>>& prob_matrix,
    const vector<int>& sorter_id_list,
    const vector<int>& processor_list
){
    int total = N + M + 1;
    int inlet_node = N + M;

    vector<vector<double>> prob(N, vector<double>(total, 0.0));
    for(int w=0; w<N; ++w) prob[w][inlet_node] = 1.0;

    for(int w=0; w<N; ++w){
        deque<int> q;
        vector<char> vis(total, 0);
        q.push_back(inlet_node);
        while(!q.empty()){
            int cur = q.front(); q.pop_front();
            if(vis[cur]) continue;
            vis[cur] = 1;
            double curp = prob[w][cur];
            if(curp == 0.0) continue;

            if(cur == inlet_node){
                if(!graph[cur].empty()){
                    int nxt = graph[cur][0];
                    prob[w][nxt] += curp;
                    q.push_back(nxt);
                }
            }else if(cur >= N){
                int sorter_idx = cur - N;
                int sorter_type = sorter_id_list[sorter_idx];
                if(sorter_type != -1 && (int)graph[cur].size() >= 2){
                    double p1 = prob_matrix[sorter_type][w];
                    double p2 = 1.0 - p1;
                    int n1 = graph[cur][0];
                    int n2 = graph[cur][1];
                    prob[w][n1] += curp * p1;
                    prob[w][n2] += curp * p2;
                    q.push_back(n1);
                    q.push_back(n2);
                }
                // 処理装置は終端
            }
        }
    }

    vector<double> correct_probs(N, 0.0);
    for(int w=0; w<N; ++w){
        double cp = 0.0;
        for(int pi=0; pi<N; ++pi){
            if(processor_list[pi] == w) cp += prob[w][pi];
        }
        correct_probs[w] = cp;
    }

    double err_sum = 0.0;
    for(int w=0; w<N; ++w) err_sum += (1.0 - correct_probs[w]);

    long long absolute_score = llround(1e9 * (err_sum / N));
    return absolute_score;
}

vector<vector<int>> make_binary_tree(
    int N, int M,
    const vector<pii>& d_coord_list,
    const vector<pii>& s_coord_list
){
    vector<vector<int>> graph(N + M + 1); // [処理装置(N), 分別器(M), 搬入口(1)]

    const int HEIGHT = X07;
    if(HEIGHT < 1) return graph;

    const int REQUIRED_SORTERS = (1<<HEIGHT) - 1;   // 2^H - 1
    const int LEAF_COUNT      = (1<<(HEIGHT-1));    // 2^(H-1)
    if(M < REQUIRED_SORTERS){
        // フォールバック
        if(M == 0 || N == 0) return graph;
        graph[N+M] = { N };           // inlet -> sorter(0番)
        graph[N]   = { 0, (N==1 ? 0 : 1%N) }; // sorter(0) -> processors
        return graph;
    }

    auto coord = [&](int node_id)->pii{
        if(node_id == N + M) return INLET;
        if(node_id < N) return d_coord_list[node_id];
        return s_coord_list[node_id - N];
    };

    vector<pair<int,int>> edges; // (u, v) ノードID

    auto edge_crosses = [&](int u, int v)->bool{
        pii cu = coord(u), cv = coord(v);
        for(auto &e : edges){
            int a = e.first, b = e.second;
            if(u==a || u==b || v==a || v==b) continue; // 端点共有は許容
            if(segments_intersect_inclusive(cu, cv, coord(a), coord(b))) return true;
        }
        return false;
    };

    vector<int> idxs(M);
    iota(idxs.begin(), idxs.end(), 0);
    auto sq = [&](ll x){ return x*x; };
    sort(idxs.begin(), idxs.end(), [&](int i, int j){
        ll dx1 = s_coord_list[i].first  - INLET.first;
        ll dy1 = s_coord_list[i].second - INLET.second;
        ll dx2 = s_coord_list[j].first  - INLET.first;
        ll dy2 = s_coord_list[j].second - INLET.second;
        return dx1*dx1 + dy1*dy1 < dx2*dx2 + dy2*dy2;
    });

    vector<int> root_candidates;
    for(int i=0;i<(int)idxs.size() && (int)root_candidates.size()<8;i++) root_candidates.push_back(idxs[i]);

    const int INTERNAL = REQUIRED_SORTERS - LEAF_COUNT; // 2^{H-1} - 1
    const int LIMIT_PAIR_TRY = 40;

    auto build_with_root = [&](int root_sorter_idx)->bool{
        vector<int> tree_order(REQUIRED_SORTERS, -1); // s_coord_list 上の index を格納
        vector<char> used(M, 0);

        tree_order[0] = root_sorter_idx;
        used[root_sorter_idx] = 1;
        edges.clear();
        edges.emplace_back(N+M, N+root_sorter_idx); // inlet -> root

        function<bool(int)> dfs = [&](int i)->bool{
            if(i >= INTERNAL) return true;
            int parent_sorter_idx = tree_order[i];
            int parent_node = N + parent_sorter_idx;
            auto pc = s_coord_list[parent_sorter_idx];

            vector<int> cand;
            for(int j: idxs) if(!used[j]) cand.push_back(j);
            sort(cand.begin(), cand.end(), [&](int a, int b){
                ll dx1 = s_coord_list[a].first - pc.first;
                ll dy1 = s_coord_list[a].second - pc.second;
                ll dx2 = s_coord_list[b].first - pc.first;
                ll dy2 = s_coord_list[b].second - pc.second;
                return dx1*dx1 + dy1*dy1 < dx2*dx2 + dy2*dy2;
            });

            vector<int> upper, lower, ordered;
            for(int j: cand){
                if(s_coord_list[j].second <= pc.second) upper.push_back(j);
                else lower.push_back(j);
            }
            size_t up=0, lo=0;
            while(up<upper.size() || lo<lower.size()){
                if(up<upper.size()) ordered.push_back(upper[up++]);
                if(lo<lower.size()) ordered.push_back(lower[lo++]);
            }
            cand.swap(ordered);

            int tries = 0;
            int L = (int)cand.size();
            for(int a_idx=0; a_idx<min(L, LIMIT_PAIR_TRY); ++a_idx){
                for(int b_idx=a_idx+1; b_idx<min(L, a_idx+1+LIMIT_PAIR_TRY); ++b_idx){
                    int a = cand[a_idx], b = cand[b_idx];
                    int node_a = N + a;
                    int node_b = N + b;

                    if(edge_crosses(parent_node, node_a)) continue;
                    edges.emplace_back(parent_node, node_a);
                    bool cross_b = edge_crosses(parent_node, node_b);
                    if(cross_b){
                        edges.pop_back();
                        continue;
                    }
                    edges.emplace_back(parent_node, node_b);

                    int c1_pos = 2*i + 1;
                    int c2_pos = 2*i + 2;
                    tree_order[c1_pos] = a;
                    tree_order[c2_pos] = b;
                    used[a] = used[b] = 1;

                    if(dfs(i+1)) return true;

                    used[a] = used[b] = 0;
                    tree_order[c1_pos] = tree_order[c2_pos] = -1;
                    edges.pop_back(); // parent->b
                    edges.pop_back(); // parent->a

                    tries++;
                    if(tries > LIMIT_PAIR_TRY) break;
                }
                if(tries > LIMIT_PAIR_TRY) break;
            }
            return false;
        };

        if(!dfs(0)){
            edges.clear();
            return false;
        }

        // 内部ノードの辺を graph へ
        graph[N+M] = { N + tree_order[0] };
        for(int i2=0;i2<INTERNAL;i2++){
            int left  = tree_order[2*i2+1];
            int right = tree_order[2*i2+2];
            graph[N + tree_order[i2]] = { N + left, N + right };
        }

        // 葉の処理：各葉から処理装置へ非交差で2本ずつ
        vector<int> leaf_indices(tree_order.begin()+INTERNAL, tree_order.end());
        sort(leaf_indices.begin(), leaf_indices.end(), [&](int a, int b){
            return s_coord_list[a].first < s_coord_list[b].first;
        });

        vector<vector<int>> proc_candidates(leaf_indices.size());
        for(size_t idx=0; idx<leaf_indices.size(); ++idx){
            int si = leaf_indices[idx];
            auto sc = s_coord_list[si];
            vector<int> order(N);
            iota(order.begin(), order.end(), 0);
            sort(order.begin(), order.end(), [&](int p, int q){
                ll dx1 = d_coord_list[p].first - sc.first;
                ll dy1 = d_coord_list[p].second - sc.second;
                ll dx2 = d_coord_list[q].first - sc.first;
                ll dy2 = d_coord_list[q].second - sc.second;
                return dx1*dx1 + dy1*dy1 < dx2*dx2 + dy2*dy2;
            });
            proc_candidates[idx] = move(order);
        }

        vector<pair<int,int>> chosen_pairs(leaf_indices.size(), {-1,-1});

        function<bool(size_t)> dfs_leaf = [&](size_t idx_leaf)->bool{
            if(idx_leaf == leaf_indices.size()) return true;
            int sorter_idx = leaf_indices[idx_leaf];
            int leaf_node = N + sorter_idx;
            auto &cands = proc_candidates[idx_leaf];

            for(size_t i1=0;i1<cands.size();++i1){
                int p1 = cands[i1];
                if(edge_crosses(leaf_node, p1)) continue;
                edges.emplace_back(leaf_node, p1);

                vector<int> order_second;
                order_second.reserve(cands.size());
                for(size_t j=0;j<cands.size();++j) if((int)j != (int)i1) order_second.push_back(cands[j]);
                order_second.push_back(p1);

                bool progressed=false;
                for(int p2 : order_second){
                    if(edge_crosses(leaf_node, p2)) continue;
                    edges.emplace_back(leaf_node, p2);
                    chosen_pairs[idx_leaf] = {p1, p2};
                    if(dfs_leaf(idx_leaf+1)) return true;
                    edges.pop_back(); // remove p2
                    progressed=true;
                }
                edges.pop_back(); // remove p1
                (void)progressed;
            }
            return false;
        };

        if(!dfs_leaf(0)){
            // sorter間の既存エッジだけ残す: 1 (inlet-root) + 2*INTERNAL
            while((int)edges.size() > 1 + 2*INTERNAL) edges.pop_back();
            return false;
        }

        for(size_t idx=0; idx<leaf_indices.size(); ++idx){
            int sorter_idx = leaf_indices[idx];
            int p1 = chosen_pairs[idx].first;
            int p2 = chosen_pairs[idx].second;
            graph[N + sorter_idx] = { p1, p2 };
        }
        return true;
    };

    bool built = false;
    for(int r : root_candidates){
        if(build_with_root(r)){ built = true; break; }
    }

    if(!built){
        // どの root でも失敗: フォールバック
        if(M == 0 || N == 0) return graph;
        graph[N+M] = { N };
        graph[N]   = { 0, (N==1 ? 0 : 1%N) };
    }

    return graph;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M, K;
    if(!(cin >> N >> M >> K)) return 0;

    vector<pii> d_coord_list(N), s_coord_list(M);
    for(int i=0;i<N;i++){
        cin >> d_coord_list[i].first >> d_coord_list[i].second;
    }
    for(int i=0;i<M;i++){
        cin >> s_coord_list[i].first >> s_coord_list[i].second;
    }

    vector<vector<double>> prob_matrix(K, vector<double>(N, 0.0));
    for(int i=0;i<K;i++){
        for(int j=0;j<N;j++){
            cin >> prob_matrix[i][j];
        }
    }

    vector<int> processor_list(N);
    iota(processor_list.begin(), processor_list.end(), 0);

    uniform_int_distribution<int> distK(0, max(0, K-1));
    vector<int> sorter_id_list(M);
    for(int i=0;i<M;i++) sorter_id_list[i] = distK(rng);

    auto graph = make_binary_tree(N, M, d_coord_list, s_coord_list);

    auto start = chrono::steady_clock::now();
    long long score = calc_score(N, M, K, graph, prob_matrix, sorter_id_list, processor_list);

    double temperature = 1.0;
    const double cooling_rate = 0.99;
    uniform_real_distribution<double> dist01(0.0, 1.0);

    while(true){
        auto now = chrono::steady_clock::now();
        double elapsed = chrono::duration<double>(now - start).count();
        if(elapsed >= TIME_LIMIT) break;

        vector<int> new_sorter_id_list = sorter_id_list;
        for(int i=0;i<M;i++){
            if(dist01(rng) < temperature){
                new_sorter_id_list[i] = distK(rng);
            }
        }
        auto new_graph = make_binary_tree(N, M, d_coord_list, s_coord_list);
        long long new_score = calc_score(N, M, K, new_graph, prob_matrix, new_sorter_id_list, processor_list);
        if(new_score < score){
            sorter_id_list.swap(new_sorter_id_list);
            graph.swap(new_graph);
            score = new_score;
        }
        temperature *= cooling_rate;
    }

    // 出力
    for(int i=0;i<N;i++){
        if(i) cout << ' ';
        cout << processor_list[i];
    }
    cout << '\n';

    // 搬入口の行き先（単一ノード）
    if(!graph[N+M].empty()) cout << graph[N+M][0] << '\n';
    else cout << 0 << '\n'; // 念のため（通常は到達しない）

    for(int i=0;i<M;i++){
        const auto& g = graph[N + i];
        if((int)g.size() < 2){
            cout << -1 << '\n';
        }else{
            cout << sorter_id_list[i] << ' ' << g[0] << ' ' << g[1] << '\n';
        }
    }
    return 0;
}
