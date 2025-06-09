#include <bits/stdc++.h>
using namespace std;

/*――――――――――  定数とグローバル ――――――――――*/
const int N = 20;                 // パレットは固定で 20×20
int  well_size  = 2;              // 1 ウェル辺のマス数
int  wells_num  = N * N / (2 * 2);

/*――――――――――  データ構造 ――――――――――*/
struct Well {
    int    amount;                // 絵の具の量（整数グラム）
    double c, m, y;               // 現在の CMY
};
using CMY = array<double, 3>;

/*――――――――――  便利関数 ――――――――――*/
// 座標変換（ウェル index → 左上マス座標）
inline pair<int,int> well_coord(int idx){
    int x = (idx / (N / well_size)) * well_size;
    int y = (idx % (N / well_size)) * well_size;
    return {x, y};
}
// コマンド文字列生成
string add_paint(int well_index, int paint_index){
    auto [x, y] = well_coord(well_index);
    return "1 " + to_string(x) + ' ' + to_string(y) + ' ' + to_string(paint_index);
}
string extract_color(int well_index){
    auto [x, y] = well_coord(well_index);
    return "2 " + to_string(x) + ' ' + to_string(y);
}
string discard_paint(int well_index){
    auto [x, y] = well_coord(well_index);
    return "3 " + to_string(x) + ' ' + to_string(y);
}
// CMY 距離
inline double calc_diff(const CMY& a, const CMY& b){
    double dc = a[0]-b[0], dm = a[1]-b[1], dy = a[2]-b[2];
    return sqrt(dc*dc + dm*dm + dy*dy);
}
// パレット内で最も近い色を探す
pair<int,double> find_nearest_color(const vector<Well>& palette, const CMY& target){
    int    nearest = -1;
    double best    = 1e100;
    for(int i=0;i<(int)palette.size();++i){
        if(palette[i].amount < 1) continue;
        CMY cur = {palette[i].c, palette[i].m, palette[i].y};
        double d = calc_diff(cur, target);
        if(d < best){ best = d; nearest = i; }
    }
    return {nearest, best};
}
// ウェルに絵の具を加える（戻り値は discard 数／容量超過時は -1）
int add_to_palette(vector<Well>& palette, int idx, const CMY& owm, int amount){
    if (amount == 0) return 0;  // 追加量が0なら何もしない
    int discard_cnt = 0;
    for(int t=0; t<amount; ++t){
        if(well_size*well_size < palette[idx].amount + amount){
            --palette[idx].amount;
            ++discard_cnt;
        }
    }
    int prev_amount = palette[idx].amount;
    int new_amount  = prev_amount + amount;
    if(new_amount > well_size*well_size) return -1;

    double nc = (palette[idx].c * prev_amount + owm[0] * amount) / new_amount;
    double nm = (palette[idx].m * prev_amount + owm[1] * amount) / new_amount;
    double ny = (palette[idx].y * prev_amount + owm[2] * amount) / new_amount;
    palette[idx] = {new_amount, nc, nm, ny};
    return discard_cnt;
}

/*――――――――――  main ――――――――――*/
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    /* 入力 */
    int N_in, K, H, T, D;
    cin >> N_in >> K >> H >> T >> D;
    vector<CMY> owm_list(K), target_list(H);
    for(auto& v: owm_list)   cin >> v[0] >> v[1] >> v[2];
    for(auto& v: target_list) cin >> v[0] >> v[1] >> v[2];

    /* 初期仕切り（2×2 ウェルを作成） */
    vector<vector<int>> v_list(N,   vector<int>(N-1, 0));
    vector<vector<int>> h_list(N-1, vector<int>(N,   0));
    for(int j=0;j<N-1;++j) if((j+1)%well_size==0){
        for(int i=0;i<N;++i){
            v_list[i][j] = 1;
            h_list[j][i] = 1;      // Python 原作と同じ挙動
        }
    }

    /* 出力用バッファ */
    vector<string> lines;          // 最終的に cout する全行
    // 仕切り（縦 → 横）
    for(int i=0;i<N;++i){
        string s;
        for(int j=0;j<N-1;++j){
            s += char('0' + v_list[i][j]);
            if(j != N-2) s += ' ';
        }
        lines.push_back(move(s));
    }
    for(int i=0;i<N-1;++i){
        string s;
        for(int j=0;j<N;++j){
            s += char('0' + h_list[i][j]);
            if(j != N-1) s += ' ';
        }
        lines.push_back(move(s));
    }

    /* パレット準備：全 100 ウェルを 4g ずつランダムで初期充填 */
    mt19937 rng(1317);
    uniform_int_distribution<int> randK(0, K-1);

    vector<Well> palette(wells_num, {0,0.0,0.0,0.0});
    int add_count = 0;
    for(int w=0; w<wells_num; ++w){
        for(int t=0; t<well_size*well_size-2; ++t){  // 1ウェルあたり1グラムは開けておく
            int k = randK(rng);
            add_to_palette(palette, w, owm_list[k], 1);
            lines.push_back(add_paint(w, k));
            add_count++;  // add_countの追加をここに移動
        }
    }
    // add_count += N * N;            // 400 g 追加済み

    double trans_prob = 1.0 - pow(1.0 / wells_num, 1.0 / wells_num);  // 遷移確率
    // 0から1の乱数
    uniform_real_distribution<double> rand01(0.0, 1.0);
    /* 目標 1000 色を順に処理 */
    double total_diff = 0.0;
    for(const auto& target : target_list){
        int trans_count = 0;  // コストが同じ場合の遷移が行われた回数
        int j_start = 0;  // jの開始値

        double best_cost         = 1e100;
        vector<Well> best_pal;
        int best_j               = -1;
        double best_diff         = 0.0;
        int best_discard_cnt     = 0;
        int best_well_idx_to_add = -1;
        int best_paint_idx       = -1;
        int best_extract_well    = -1;

        /* 探索（100 ウェル × K 色 × 1or2g） */
        for(int wi=0; wi<wells_num; ++wi){
            for(int pk=0; pk<K; ++pk){
                for(int j=j_start; j<=2; ++j){
                    vector<Well> tmp_pal = palette;
                    int discard_cnt = add_to_palette(tmp_pal, wi, owm_list[pk], j);
                    if(discard_cnt == -1) continue;            // 容量超過

                    auto [near_idx, diff] = find_nearest_color(tmp_pal, target);
                    if(near_idx == -1) continue;

                    double cost = D * (j - 1) + diff * 1e4;
                    if(cost <= best_cost){
                        // コストが同じならtrans_prob * (1 - 0.2*trans_count)の確率で遷移
                        if(cost == best_cost){
                            if(rand01(rng) > trans_prob * (1 - 0.2 * trans_count)){
                                continue;
                            }
                            else{
                                trans_count++;  // 遷移が行われた回数を増やす
                            }
                        }
                        best_cost         = cost;
                        best_pal          = move(tmp_pal);
                        best_j            = j;
                        best_diff         = diff;
                        best_discard_cnt  = discard_cnt;
                        best_well_idx_to_add = wi;
                        best_paint_idx    = pk;
                        best_extract_well = near_idx;
                    }
                }
            }
        }

        /* コマンド生成 */
        for(int d=0; d<best_discard_cnt; ++d)
            lines.push_back(discard_paint(best_well_idx_to_add));
        for(int t=0; t<best_j; ++t)
            lines.push_back(add_paint(best_well_idx_to_add, best_paint_idx));
        lines.push_back(extract_color(best_extract_well));

        /* パレット更新 */
        if(best_extract_well >= 0)
            --best_pal[best_extract_well].amount;
        palette.swap(best_pal);
        add_count   += best_j;
        total_diff  += best_diff;
    }

    /* すべて出力 */
    for(const string& s : lines) cout << s << '\n';
    return 0;
}
