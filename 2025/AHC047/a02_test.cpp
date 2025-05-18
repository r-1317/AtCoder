//  ------------------------------------
//  Lovely Language Model  –  C++17 版
//  ------------------------------------
#include <bits/stdc++.h>
using namespace std;

constexpr int N = 36;
constexpr int M = 12;
constexpr long long L = 1'000'000;
const string ALPHA = "abcdef";
int alpha_idx(char c) { return c - 'a'; }

//--------------------------------------
// KMP 風オートマトン (6 文字アルファベット用)
// nxt[k][c] = 「いま prefix 長が k で文字 c を読んだら
//              何文字目まで prefix が一致しているか」
//--------------------------------------
vector<vector<int>> build_kmp_next(const string& pat) {
    int m = (int)pat.size();
    vector<vector<int>> nxt(m + 1, vector<int>(6, 0));

    for (int k = 0; k <= m; ++k) {
        for (int ci = 0; ci < 6; ++ci) {
            char ch = 'a' + ci;
            int l = min(m, k + 1);
            string prefix = pat.substr(0, k);
            prefix.push_back(ch);          // pat[:k] + ch
            while (l > 0) {
                if (pat.substr(0, l) ==
                    prefix.substr(prefix.size() - l))
                    break;
                --l;
            }
            nxt[k][ci] = l;
        }
    }
    return nxt;
}

//--------------------------------------
// 疎行列ベクトル積 v * T
//--------------------------------------
using SparseMat = vector<unordered_map<int, double>>;

vector<double> vec_mul(const vector<double>& v, const SparseMat& T) {
    int n = (int)v.size();
    vector<double> nv(n, 0.0);
    for (int i = 0; i < n; ++i) if (v[i] != 0.0) {
        for (auto [j, p] : T[i]) nv[j] += v[i] * p;
    }
    return nv;
}

//--------------------------------------
// 疎行列乗算  C = A * B
//--------------------------------------
SparseMat mat_mul(const SparseMat& A, const SparseMat& B) {
    int n = (int)A.size();
    SparseMat C(n);
    for (int i = 0; i < n; ++i) {
        for (auto [k, aik] : A[i]) {
            for (auto [j, bkj] : B[k]) {
                C[i][j] += aik * bkj;
            }
        }
    }
    return C;
}

//--------------------------------------
// 文字列 pat に対する
//   ・未ヒット状態だけからなる遷移行列 T
//   ・初期ベクトル v0
//--------------------------------------
pair<SparseMat, vector<double>>
build_transition(const string& pat,
                 const vector<char>& state_list,
                 const vector<array<int, M>>& prob_matrix)
{
    int m = (int)pat.size();
    auto nxt = build_kmp_next(pat);
    int size = m * M;
    SparseMat T(size);          // size 行

    for (int prog = 0; prog < m; ++prog) {
        for (int s = 0; s < M; ++s) {
            int fr = prog * M + s;
            for (int t = 0; t < M; ++t) {
                if (prob_matrix[s][t] == 0) continue;
                double p = prob_matrix[s][t] / 100.0;
                char ch = state_list[t];
                int np = nxt[prog][alpha_idx(ch)];
                if (np == m) continue;                 // ヒット後の状態は作らない
                int to = np * M + t;
                T[fr][to] += p;
            }
        }
    }
    int first_prog = nxt[0][alpha_idx(state_list[0])];
    if (first_prog == m) {        // 1 文字目でヒット
        return {T, {}};           // 空ベクトルで「既にヒットした」ことを示す
    }
    vector<double> v0(size, 0.0);
    v0[first_prog * M + 0] = 1.0;
    return {T, v0};
}

//--------------------------------------
// v * T^steps を計算し、要素和 (=未ヒット確率) を返す
//--------------------------------------
double power_vector(vector<double> v,
                    SparseMat T,
                    long long steps)
{
    if (steps == 0) return accumulate(v.begin(), v.end(), 0.0);
    while (steps) {
        if (steps & 1) v = vec_mul(v, T);
        steps >>= 1;
        if (steps) T = mat_mul(T, T);
    }
    return accumulate(v.begin(), v.end(), 0.0);
}

//--------------------------------------
// スコア計算 (デバッグ用)
//--------------------------------------
long long calc_score(const vector<string>& s_list,
                     const vector<int>& p_list,
                     const vector<char>& state_list,
                     const vector<array<int, M>>& prob_matrix)
{
    long double total = 0.0;
    const long long rem_steps = L - 1;
    for (int idx = 0; idx < N; ++idx) {
        const string& pat = s_list[idx];
        auto [T, v0] = build_transition(pat, state_list, prob_matrix);
        long double Qi;
        if (v0.empty()) {
            Qi = 1.0;                         // 初手でヒット
        } else {
            long double nohit = power_vector(v0, T, rem_steps);
            Qi = 1.0 - nohit;
        }
        total += p_list[idx] * Qi;
    }
    return llround(total);
}

//--------------------------------------
// メイン
//--------------------------------------
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // --- 入力 ---
    int dummyN, dummyM;
    long long dummyL;
    cin >> dummyN >> dummyM >> dummyL;        // 実際には固定値
    vector<string> s_list(N);
    vector<int>    p_list(N);
    for (int i = 0; i < N; ++i) {
        cin >> s_list[i] >> p_list[i];
    }

    // --- 状態文字 ---
    vector<char> state_list = {
        'a','b','c','d','e','f',
        'a','b','c','d','e','f'
    };

    // --- 遷移確率行列 ---
    //   prob_matrix[i][j] : 状態 i → j の確率 (百分率整数)
    vector<array<int, M>> prob_matrix(6);            // 前半 6 行 (初期は 0)
    const array<int, M> PADDING = {9,9,9,9,8,8,8,8,8,8,8,8};
    for (int i = 6; i < M; ++i) prob_matrix.push_back(PADDING);

    // --- 文字列から重み付き遷移を集計 ---
    double trans_pt[6][6] = {};
    for (int idx = 0; idx < N; ++idx) {
        const string& s = s_list[idx];
        int len = (int)s.size();
        double w = (double)p_list[idx] / len;
        for (int j = 0; j + 1 < len; ++j) {
            int a = alpha_idx(s[j]);
            int b = alpha_idx(s[j+1]);
            trans_pt[a][b] += w;
        }
    }

    // --- 行正規化 (整数化) ---
    std::mt19937 rng((unsigned)chrono::steady_clock::now().time_since_epoch().count());
    for (int i = 0; i < 6; ++i) {
        double row_sum = 0.0;
        for (int j = 0; j < 6; ++j) row_sum += trans_pt[i][j];

        int rowTotal = 0;
        if (row_sum > 0) {
            for (int j = 0; j < 6; ++j) {
                int v = (int)(trans_pt[i][j] / row_sum * 100.0);
                prob_matrix[i][j] = v;
                rowTotal += v;
            }
        }
        // 残差をランダムに振って 100 に合わせる
        for (int k = 0; k < 100 - rowTotal; ++k) {
            int j = rng() % 6;
            ++prob_matrix[i][j];
        }
    }

    // --- (オプション) スコア計算 ---
    // long long score = calc_score(s_list, p_list, state_list, prob_matrix);
    // cerr << "estimated score = " << score << "\n";

    // --- 出力 ---
    for (int i = 0; i < M; ++i) {
        cout << state_list[i];
        for (int j = 0; j < M; ++j) cout << ' ' << prob_matrix[i][j];
        cout << '\n';
    }
    return 0;
}
