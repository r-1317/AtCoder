// ------------------------------------------------------------
// Lovely Language Model  –  heuristic solver (C++17 port)
//   original Python code written by user, ported by ChatGPT
// ------------------------------------------------------------
#include <bits/stdc++.h>
using namespace std;

using ld = double;

// ----------------- 乱数 -----------------
static mt19937 rng(1317);                 // 固定シード
inline int rnd_int(int l, int r) {        //  l <= x <= r
    uniform_int_distribution<int> dist(l, r);
    return dist(rng);
}

// ----------------- 定数 -----------------
constexpr int N = 36;       // 文字列数
constexpr int M = 12;       // 状態数
constexpr long long L = 1'000'000;   // 出力長
constexpr int ALPHA_SZ = 6;          // a–f

// a〜f を添字に変換するテーブル
array<int, 256> build_alpha_idx() {
    array<int, 256> idx{};
    idx.fill(-1);
    const string alpha = "abcdef";
    for (int i = 0; i < 6; ++i) idx[(unsigned char)alpha[i]] = i;
    return idx;
}
const array<int, 256> ALPHA_IDX = build_alpha_idx();

// ============================================================
// KMP「次状態」テーブル:  next[k][c] = prefix length after
// 既に長さ k マッチしている状態で文字 c を読むとどう進むか
// 文字種類は 6 種だけなので素朴に作っても十分高速
// ============================================================
vector<array<int, ALPHA_SZ>> build_kmp_next(const string& pat) {
    int m = (int)pat.size();
    vector<array<int, ALPHA_SZ>> nxt(m + 1);
    for (int k = 0; k <= m; ++k) {
        for (int ci = 0; ci < ALPHA_SZ; ++ci) {
            int l = min(m, k + 1);
            while (l > 0) {
                bool ok = true;
                for (int t = 0; t < l; ++t) {
                    char x = (k + t < (int)pat.size()) ? pat[t] : char('a' + ci);
                    char y;
                    if (l - t - 1 < k)
                        y = pat[k - (l - t - 1) - 1];
                    else
                        y = char('a' + ci);
                    if (x != y) { ok = false; break; }
                }
                if (ok) break;
                --l;
            }
            nxt[k][ci] = l;
        }
    }
    return nxt;
}

// ------------------------------------------------------------
// 疎ベクトル × 疎行列 (行列は隣接リスト形式) 演算
// ------------------------------------------------------------
using SparseRow = unordered_map<int, ld>;             // 列 -> 値
using SparseMat = vector<SparseRow>;                  // 行ごとの疎ベクトル
using Vec       = vector<ld>;

Vec vec_mul(const Vec& v, const SparseMat& T) {
    int n = (int)v.size();
    Vec nv(n, 0.0);
    for (int i = 0; i < n; ++i) if (v[i] != 0.0) {
        for (auto [j, pij] : T[i])
            nv[j] += v[i] * pij;
    }
    return nv;
}

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

// ------------------------------------------------------------
// パターンごとに「まだ出現していない」状態のみで遷移行列を作る
//   戻り値: (T, v0)   v0.size()==0 のときは初手でヒット確定
// ------------------------------------------------------------
pair<SparseMat, Vec> build_transition(
        const string& pat,
        const vector<char>& state_list,
        const vector<array<int, M>>& prob_mat)
{
    int m = (int)pat.size();
    auto nxt = build_kmp_next(pat);

    const int SZ = m * M;
    SparseMat T(SZ);

    for (int prog = 0; prog < m; ++prog) {
        for (int s = 0; s < M; ++s) {
            int fr = prog * M + s;
            for (int t = 0; t < M; ++t) {
                int p_int = prob_mat[s][t];
                if (p_int == 0) continue;
                ld p = p_int / 100.0;
                char ch = state_list[t];
                int np = nxt[prog][ALPHA_IDX[(unsigned char)ch]];
                if (np == m) continue;                 // ここで pat 完了 → NG
                int to = np * M + t;
                T[fr][to] += p;
            }
        }
    }

    int first_prog = nxt[0][ALPHA_IDX[(unsigned char)state_list[0]]];
    if (first_prog == m) {          // いきなりヒット
        return { T, Vec() };        // v0 空ベクトルで特別扱い
    }
    Vec v0(SZ, 0.0);
    v0[first_prog * M + 0] = 1.0;   // 開始位置は状態 0
    return { T, v0 };
}

// ------------------------------------------------------------
// v * T^steps を求め、要素和 (= ヒットしてない確率) を返す
// ------------------------------------------------------------
ld power_vector(Vec v, const SparseMat& T, long long steps) {
    if (steps == 0) {
        ld s = accumulate(v.begin(), v.end(), 0.0);
        return s;
    }
    vector<SparseMat> mats;
    mats.reserve(64);
    mats.push_back(T);
    int k = 0;
    while ((1LL << (k + 1)) <= steps) {
        mats.push_back(mat_mul(mats[k], mats[k]));
        ++k;
    }
    int idx = 0;
    while (steps) {
        if (steps & 1LL) v = vec_mul(v, mats[idx]);
        steps >>= 1LL;
        ++idx;
    }
    ld s = accumulate(v.begin(), v.end(), 0.0);
    return s;
}

// ------------------------------------------------------------
// 与えられたモデルでの期待スコアを計算
// ------------------------------------------------------------
int calc_score(const vector<string>& s_list,
               const vector<int>& p_list,
               const vector<char>& state_list,
               const vector<array<int, M>>& prob_mat)
{
    long long rem_steps = L - 1;
    ld total = 0.0;
    for (int idx = 0; idx < N; ++idx) {
        const string& pat = s_list[idx];
        int P            = p_list[idx];
        auto [T, v0]     = build_transition(pat, state_list, prob_mat);
        ld Qi;
        if (v0.empty()) {
            Qi = 1.0;                            // 初手確定ヒット
        } else {
            ld nohit = power_vector(v0, T, rem_steps);
            Qi = 1.0 - nohit;
        }
        total += P * Qi;
    }
    return int(std::llround(total));
}

// ------------------------------------------------------------
// 遷移確率行列をランダムに小変更（山登り用）
// ------------------------------------------------------------
void random_change(vector<array<int, M>>& mat) {
    constexpr int X = 4;
    constexpr int Y = 3;
    for (int i = 0; i < M; ++i) {
        for (int rep = 0; rep < Y; ++rep) {
            int j = rnd_int(0, M - 1);
            int k = rnd_int(0, M - 1);
            if (mat[i][j] < X) continue;
            mat[i][j] -= X;
            mat[i][k] += X;
        }
    }
}

// ------------------------------------------------------------
// 行列を出力（12 行）
// ------------------------------------------------------------
void output_solution(const vector<char>& state_list,
                     const vector<array<int, M>>& prob_mat)
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    for (int i = 0; i < M; ++i) {
        cout << state_list[i];
        for (int j = 0; j < M; ++j) cout << ' ' << prob_mat[i][j];
        cout << '\n';
    }
    cout.flush();
}

// ============================================================
//                         main
// ============================================================
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // --- 入力 ---
    int Ni, Mi;
    long long Li;
    cin >> Ni >> Mi >> Li;
    vector<string> s_list(N);
    vector<int> p_list(N);
    for (int i = 0; i < N; ++i) cin >> s_list[i] >> p_list[i];

    // --- ベースとなる文字列（好ましさ最大）を採用 ---
    int max_p = -1;
    string best_s;
    for (int i = 0; i < N; ++i) {
        if (p_list[i] > max_p) { max_p = p_list[i]; best_s = s_list[i]; }
    }

    // --- 状態に文字を割り当てる ---
    vector<char> state_list(M);
    for (size_t i = 0; i < best_s.size(); ++i) state_list[i] = best_s[i];
    for (int i = (int)best_s.size(); i < M; ++i)
        state_list[i] = char('a' + rnd_int(0, 5));

    // --- 遷移確率行列の初期化 ---
    vector<array<int, M>> prob_mat(M);
    for (auto& row : prob_mat) row.fill(5);          // 基本 5%

    for (int i = 0; i < M; ++i) {
        if (i < (int)best_s.size() - 1) {
            prob_mat[i][i + 1] += 40;                // 直列化
        } else {
            for (int j = 0; j < M; ++j) prob_mat[i][j] += 3;
            for (int t = 0; t < 4; ++t) {
                int j = rnd_int(0, M - 1);
                ++prob_mat[i][j];
            }
        }
        // 行和を 100 に正規化
        int sum = accumulate(begin(prob_mat[i]), end(prob_mat[i]), 0);
        for (int j = 0; j < M && sum != 100; ++j) {
            int diff = (sum > 100) ? min(sum - 100, prob_mat[i][j])
                                   : min(100 - sum, 100 - prob_mat[i][j]);
            prob_mat[i][j] += (sum > 100 ? -diff : diff);
            sum += (sum > 100 ? -diff : diff);
        }
    }

    // --- 初期スコア計算＆出力 ---
    int best_score = calc_score(s_list, p_list, state_list, prob_mat);
    output_solution(state_list, prob_mat);

    // --- 山登り (1.5 秒制限) ---
    auto t0 = chrono::steady_clock::now();
    const double TIME_LIMIT = 1.5;
    while (true) {
        auto now = chrono::steady_clock::now();
        double elapsed = chrono::duration<double>(now - t0).count();
        if (elapsed > TIME_LIMIT) break;

        // 候補を生成
        auto cand_mat = prob_mat;
        random_change(cand_mat);

        int cand_score = calc_score(s_list, p_list, state_list, cand_mat);
        if (cand_score > best_score) {
            best_score = cand_score;
            prob_mat.swap(cand_mat);
            output_solution(state_list, prob_mat);            // より良ければ出力
        }
    }
    return 0;
}
