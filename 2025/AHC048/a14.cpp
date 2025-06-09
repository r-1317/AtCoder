//  AHC048  “A - Mixing on the Palette”
//  python 版を出来るだけ忠実に C++17 へ移植

#include <bits/stdc++.h>
using namespace std;

constexpr int N          = 20;     // パレットは常に 20×20
constexpr int well_size  = 4;      // 1 ウェルの一辺
constexpr int wells_side = N / well_size;
constexpr int wells_num  = (N * N) / (well_size * well_size);

mt19937 rng(1317);

// ------------------------------------------------------------
//  基本構造体・ユーティリティ
// ------------------------------------------------------------
struct Well {
    double amount = 0;   // 絵の具量 [g]
    double c = 0, m = 0, y = 0;   // CMY
};

struct State {
    bool   visited;          // 探索済みフラグ
    double tmp_cost;         // 探索用仮コスト
    double diff;             // この step での誤差
    int    add_count;        // この step で追加した量
    vector<Well> palette;    // ウェルの状態
    vector<string> cmds;     // この step の出力行
    int    prev_index;       // 直前 State のインデックス
};

// 座標計算
inline int well_x(int idx) { return (idx / wells_side) * well_size; }
inline int well_y(int idx) { return (idx % wells_side) * well_size; }

// コマンド生成
inline string add_paint(int wi, int pi) {
    return "1 " + to_string(well_x(wi)) + ' ' + to_string(well_y(wi)) + ' ' + to_string(pi);
}
inline string extract_color(int wi) {
    return "2 " + to_string(well_x(wi)) + ' ' + to_string(well_y(wi));
}
inline string discard_paint(int wi) {
    return "3 " + to_string(well_x(wi)) + ' ' + to_string(well_y(wi));
}

// 距離計算
inline double calc_diff(const array<double,3>& a, const array<double,3>& b) {
    double dx = a[0]-b[0], dy = a[1]-b[1], dz = a[2]-b[2];
    return sqrt(dx*dx + dy*dy + dz*dz);
}

// palette から最も近い色を探す
pair<int,double> find_nearest_color(const vector<Well>& palette,
                                    const array<double,3>& target) {
    int idx = -1; double best = 1e100;
    for(int i=0;i<wells_num;++i) {
        if (palette[i].amount < 1.0) continue;
        array<double,3> cur{palette[i].c, palette[i].m, palette[i].y};
        double d = calc_diff(cur,target);
        if (d < best) { best = d; idx = i; }
    }
    return {idx,best};
}

// palette へ絵の具を追加（戻り値 = 廃棄量）
int add_to_palette(vector<Well>& palette, int wi, const array<double,3>& owm, int amt) {
    if (!amt) return 0;
    const int cap = well_size*well_size;
    int cur_int   = static_cast<int>(palette[wi].amount + 0.5);
    int can_add   = min(amt, cap - cur_int);
    int discard   = amt - can_add;

    double prev_amt = palette[wi].amount;
    double new_amt  = prev_amt + can_add;
    if (can_add) {
        palette[wi].c = (prev_amt*palette[wi].c + owm[0]*can_add) / new_amt;
        palette[wi].m = (prev_amt*palette[wi].m + owm[1]*can_add) / new_amt;
        palette[wi].y = (prev_amt*palette[wi].y + owm[2]*can_add) / new_amt;
        palette[wi].amount = new_amt;
    }
    return discard;
}

// ------------------------------------------------------------
//  本体
// ------------------------------------------------------------
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    /* 入力 */
    int inN, K, H, T;
    long long D;
    cin >> inN >> K >> H >> T >> D;

    vector<array<double,3>> owm_list(K);
    for (auto& a: owm_list) cin >> a[0] >> a[1] >> a[2];

    vector<array<double,3>> target_list(H);
    for (auto& a: target_list) cin >> a[0] >> a[1] >> a[2];

    /* 初期仕切り（4×4 のウェルを 5×5 並べる） */
    vector<string> init_lines;
    int v[N][N-1] = {};
    int h[N-1][N] = {};
    for (int j=0;j<N-1;++j) if ((j+1)%well_size==0)
        for (int i=0;i<N;++i) { v[i][j]=1; h[j][i]=1; }

    for (int i=0;i<N;++i) {
        string s;
        for (int j=0;j<N-1;++j) { s += char('0'+v[i][j]); if(j!=N-2) s+=' '; }
        init_lines.push_back(move(s));
    }
    for (int i=0;i<N-1;++i) {
        string s;
        for (int j=0;j<N;++j) { s += char('0'+h[i][j]); if(j!=N-1) s+=' '; }
        init_lines.push_back(move(s));
    }

    /* 初期パレットを適当に充填（各ウェル 4g） */
    vector<Well> palette(wells_num);
    uniform_int_distribution<int> rndK(0,K-1);
    int init_add_cnt = 0;
    for (int w=0; w<wells_num; ++w)
        for (int t=0; t<well_size*well_size/4; ++t) {
            int pi = rndK(rng);
            add_to_palette(palette,w,owm_list[pi],1);
            init_lines.push_back(add_paint(w,pi));
            ++init_add_cnt;
        }

    /* chokudai-like search */
    const int boost_limit = 900;
    vector<State> state_list;
    state_list.reserve(4000000);  // 足りなかったので増やした
    state_list.push_back({false,0.0,0.0,init_add_cnt,palette,init_lines,-1});

    vector<vector<int>> chokudai(H+1);
    chokudai[0].push_back(0);

    uniform_real_distribution<double> rand_small(0.0,0.001);
    auto t0 = chrono::steady_clock::now();

    while (chrono::duration<double>(chrono::steady_clock::now()-t0).count() < 2.75) {
        for (int ti=0; ti<H; ++ti) {
            if (chokudai[ti].empty()) continue;
            int prev_idx = chokudai[ti][0];
            State& prev  = state_list[prev_idx];
            if (prev.visited) continue;
            prev.visited = true;

            const auto& target = target_list[ti];
            const auto& baseP  = prev.palette;

            /* 追加無しパターン */
            if (ti > boost_limit) {
                auto pal = baseP;
                auto [nearest,dif] = find_nearest_color(pal,target);
                if (nearest!=-1) {
                    vector<string> cmds{extract_color(nearest)};
                    pal[nearest].amount -= 1.0;
                    state_list.push_back({false,
                                          D*(-1)+dif*1e4+rand_small(rng),
                                          dif,0,pal,cmds,prev_idx});
                    chokudai[ti+1].push_back(state_list.size()-1);
                }
            }

            /* 追加して混ぜるパターン */
            for (int wi=0; wi<wells_num; ++wi)
                for (int pi=0; pi<K; ++pi)
                    for (int add=1; add<=2; ++add) {

                        auto pal = baseP;
                        int discard = add_to_palette(pal,wi,owm_list[pi],add);
                        auto [nearest,dif] = find_nearest_color(pal,target);
                        if (nearest==-1) continue;

                        vector<string> cmds;
                        for(int d=0; d<discard; ++d) cmds.push_back(discard_paint(wi));
                        for(int a=0; a<add; ++a)   cmds.push_back(add_paint(wi,pi));
                        cmds.push_back(extract_color(nearest));
                        pal[nearest].amount -= 1.0;

                        state_list.push_back({false,
                                              D*(add-1+discard)+dif*1e4+rand_small(rng),
                                              dif,add,pal,cmds,prev_idx});
                        chokudai[ti+1].push_back(state_list.size()-1);
                    }

            /* 状態のソート & 削減 */
            auto& vec = chokudai[ti+1];
            sort(vec.begin(),vec.end(),[&](int a,int b){
                if (state_list[a].visited != state_list[b].visited)
                    return !state_list[a].visited && state_list[b].visited;
                return state_list[a].tmp_cost < state_list[b].tmp_cost;
            });
            if (vec.size() > 50) vec.resize(50);   // メモリ抑制
        }
    }

    /* ゴールが無ければフェイルセーフ */
    if (chokudai[H].empty()) {
        for (const string& s: init_lines) cout << s << '\n';
        for (int i=0; i<H; ++i) {
            cout << add_paint(0,0)   << '\n';
            cout << extract_color(0) << '\n';
        }
        return 0;
    }

    /* 最終経路を復元 */
    int cur = chokudai[H][0];
    vector<int> path;
    while (cur!=-1) { path.push_back(cur); cur = state_list[cur].prev_index; }
    reverse(path.begin(),path.end());

    long long add_sum = 0;
    double    diff_sum = 0;
    vector<string> out;
    for (int idx: path) {
        add_sum  += state_list[idx].add_count;
        diff_sum += state_list[idx].diff;
        out.insert(out.end(),
                   state_list[idx].cmds.begin(),
                   state_list[idx].cmds.end());
    }

    long long total_score = llround(1 + D*(add_sum - H) + 1e4*diff_sum);
    cerr << total_score << '\n';   // ← 必須: 標準エラーへ

    for (const string& s: out) cout << s << '\n';
    return 0;
}
