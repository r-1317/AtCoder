#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
using namespace std;
 
// 定数
const int N = 20;
 
// グリッド中の 'x'（鬼）の個数を数える関数
int count_x(const vector<string>& grid) {
    int cnt = 0;
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            if (grid[i][j] == 'x')
                cnt++;
        }
    }
    return cnt;
}
 
// グリッド中の 'o'（福）の個数を数える関数
int count_o(const vector<string>& grid) {
    int cnt = 0;
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            if (grid[i][j] == 'o')
                cnt++;
        }
    }
    return cnt;
}
 
// 盤面のコピーを作成し、指定した行または列を指定方向にシフトする。
// d: 移動方向 ('L', 'R', 'U', 'D')
// p: 移動対象の行（d=='L'または'R'の場合）または列（d=='U'または'D'の場合）のインデックス
vector<string> move_grid(const vector<string>& grid, char d, int p) {
    vector<string> new_grid = grid; // ディープコピー
    if (d == 'L') {
        // 行 p を左にシフト
        for (int i = 0; i < N - 1; i++) {
            new_grid[p][i] = grid[p][i+1];
        }
        new_grid[p][N-1] = '.';
    } else if (d == 'R') {
        // 行 p を右にシフト
        new_grid[p][0] = '.';
        for (int i = 1; i < N; i++) {
            new_grid[p][i] = grid[p][i-1];
        }
    } else if (d == 'U') {
        // 列 p を上にシフト
        for (int i = 0; i < N - 1; i++) {
            new_grid[i][p] = grid[i+1][p];
        }
        new_grid[N-1][p] = '.';
    } else if (d == 'D') {
        // 列 p を下にシフト
        new_grid[0][p] = '.';
        for (int i = 1; i < N; i++) {
            new_grid[i][p] = grid[i-1][p];
        }
    }
    return new_grid;
}
 
// 指定位置 (i,j) にある鬼（'x'）について、上下左右それぞれの方向で
// 鬼が落ちるまでの距離の 3 乗の逆数を計算し、その中で最大のものを返す。
// 途中に福（'o'）があれば、その方向は無視する。
double calc_x_eval(const vector<string>& grid, int i, int j) {
    double bestVal = 0.0;
    vector<pair<int,int>> dirs = { {0,1}, {0,-1}, {1,0}, {-1,0} };
    for (auto &dir : dirs) {
        int di = dir.first, dj = dir.second;
        int x = i, y = j;
        bool blocked = false;
        int dist = 1;
        x += di; y += dj;
        while (x >= 0 && x < N && y >= 0 && y < N) {
            if (grid[x][y] == 'o') {
                blocked = true;
                break;
            }
            if (grid[x][y] == '.')
                dist++;
            x += di; y += dj;
        }
        if (blocked) continue;
        double candidate = 1.0 / (dist * dist * dist);
        bestVal = max(bestVal, candidate);
    }
    return bestVal;
}
 
// 盤面全体の評価値を計算する関数
double calc_eval_01(const vector<string>& grid) {
    double ev = 0.0;
    // 福を落とした場合の大きなペナルティ
    ev -= 1e9 * (2 * N - count_o(grid));
    // 鬼を落とした場合の報酬
    ev += 1e5 * (2 * N - count_x(grid));
    // 各鬼について、その鬼が落ちるまでの評価を加算
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            if (grid[i][j] == 'x'){
                ev += calc_x_eval(grid, i, j);
            }
        }
    }
    return ev;
}
 
// 探索状態を表す構造体
struct State {
    bool visited;                       // すでに展開済みか
    double eval;                        // 評価値
    vector<string> grid;                // 現在の盤面
    vector<pair<char,int>> moves;       // これまでの操作の履歴 (方向, 行または列のインデックス)
};
 
// chokudaiサーチ（ビームサーチ）の実装
// 盤面と開始時刻を受け取り、全ての鬼を落とす操作列を返す（見つからなければ空のリスト）。
vector<pair<char,int>> serch_02(const vector<string>& initGrid,
    chrono::steady_clock::time_point start_time) {
    
    vector<pair<char,int>> shortestAns; // 最短の操作列
    int min_len = 4 * N * N + 1;          // 許容する最大操作回数 (4*N^2+1)
    // 各操作回数ごとの状態リスト
    vector<vector<State>> beam(4 * N * N + 1);
 
    double initEval = calc_eval_01(initGrid);
    State initState;
    initState.visited = false;
    initState.eval = initEval;
    initState.grid = initGrid;
    // 操作履歴は空で初期化
    beam[0].push_back(initState);
 
    // 実行時間が約1.9秒以内で探索する
    while (true) {
        auto now = chrono::steady_clock::now();
        double elapsed = chrono::duration<double>(now - start_time).count();
        cerr << "Elapsed time: " << elapsed << " seconds" << endl;
        if (elapsed >= 1.9)
            break;
 
        bool found = false;
        // 各操作回数（深さ）について探索
        for (int i = 0; i < min_len - 1; i++){
            if (beam[i].empty()) continue;
            // すでにこの深さの先頭状態が展開済みならスキップ
            if (beam[i][0].visited)
                continue;
 
            State cur = beam[i][0]; // 最高評価の状態を選択
 
            // 4方向すべてについて
            for (char d : {'L', 'R', 'U', 'D'}) {
                if (found) break;
                // すべての行または列 (0～N-1) に対して操作を試す
                for (int p = 0; p < N; p++){
                    vector<string> newGrid = move_grid(cur.grid, d, p);
                    double newEval = calc_eval_01(newGrid);
                    vector<pair<char,int>> newMoves = cur.moves;
                    newMoves.push_back({d, p});
 
                    State newState;
                    newState.visited = false;
                    newState.eval = newEval;
                    newState.grid = newGrid;
                    newState.moves = newMoves;
 
                    beam[i+1].push_back(newState);
 
                    // もし盤面上に鬼がなくなったなら解を記録
                    if (count_x(newGrid) == 0) {
                        min_len = i + 1;
                        shortestAns = newMoves;
                        found = true;
                        break;
                    }
                }
            }
            // 次の深さの状態リストを、未展開かつ評価値の高い順にソート
            sort(beam[i+1].begin(), beam[i+1].end(), [](const State &a, const State &b) {
                if (a.visited != b.visited)
                    return a.visited < b.visited; // false (未展開) が先
                return a.eval > b.eval; // 評価値の高い順
            });
            // 現在の状態を展開済みとする
            beam[i][0].visited = true;
            if (found)
                break;
        }
        if (!shortestAns.empty())
            break;
    }
    return shortestAns;
}
 
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
 
    // 入力
    // 最初の整数はグリッドのサイズ（ここでは20と想定）
    int n;
    cin >> n;
    vector<string> grid(n);
    for (int i = 0; i < n; i++){
        cin >> grid[i];
    }
 
    auto start_time = chrono::steady_clock::now();
    // chokudaiサーチで操作列を探索
    vector<pair<char,int>> ans = serch_02(grid, start_time);
 
    // 出力：各行に "方向 インデックス" を出力
    for (auto &mv : ans){
        cout << mv.first << " " << mv.second << "\n";
    }
 
    return 0;
}
