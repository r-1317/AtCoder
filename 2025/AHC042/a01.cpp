#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <limits>
#include <algorithm>
using namespace std;

const int N = 20;

// グリッド内の 'x' の数を数える
int count_x(const vector<vector<char>> &grid) {
    int cnt = 0;
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            if (grid[i][j] == 'x')
                cnt++;
        }
    }
    return cnt;
}

// グリッド内の 'o' の数を数える
int count_o(const vector<vector<char>> &grid) {
    int cnt = 0;
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            if (grid[i][j] == 'o')
                cnt++;
        }
    }
    return cnt;
}

// 盤面の1行または1列を d の方向に動かす関数
vector<vector<char>> moveGrid(const vector<vector<char>> &grid, char d, int p) {
    vector<vector<char>> new_grid = grid; // 深いコピー
    if (d == 'L') {
        // 行 p を左に動かす
        for (int j = 0; j < N - 1; j++){
            new_grid[p][j] = grid[p][j+1];
        }
        new_grid[p][N-1] = '.';  // 一番右は空白にする
    }
    else if (d == 'R') {
        // 行 p を右に動かす
        new_grid[p][0] = '.';  // 一番左は空白にする
        for (int j = 1; j < N; j++){
            new_grid[p][j] = grid[p][j-1];
        }
    }
    else if (d == 'U') {
        // 列 p を上に動かす
        for (int i = 0; i < N - 1; i++){
            new_grid[i][p] = grid[i+1][p];
        }
        new_grid[N-1][p] = '.';  // 一番下は空白にする
    }
    else if (d == 'D') {
        // 列 p を下に動かす
        new_grid[0][p] = '.';  // 一番上は空白にする
        for (int i = 1; i < N; i++){
            new_grid[i][p] = grid[i-1][p];
        }
    }
    return new_grid;
}
 
// 指定した位置 (i, j) の x について、上下左右4方向で
// 鬼（'x'）が落ちるまでの距離のM乗の逆数の最大値を計算する
long double calc_x_eval(const vector<vector<char>> &grid, int i, int j) {
    long double bestEval = 0.0L;
    // 4方向 (右, 左, 下, 上)
    vector<pair<int,int>> directions = { {0,1}, {0,-1}, {1,0}, {-1,0} };
    for (auto &dir : directions) {
        int di = dir.first, dj = dir.second;
        int x = i, y = j;
        bool blockedByO = false;
        int dist = 1;
        // 1ステップ進める
        x += di; y += dj;
        while (x >= 0 && x < N && y >= 0 && y < N) {
            if (grid[x][y] == 'o') {
                blockedByO = true;
                break;
            }
            if (grid[x][y] == '.')
                dist++;
            x += di;
            y += dj;
        }
        // もし経路上に 'o' があればこの方向は採用しない
        if (blockedByO) continue;
        long double curEval = 1.0L / ((long double)dist * dist * dist * dist);
        bestEval = max(bestEval, curEval);
    }
    return bestEval;
}
 
// 現在の盤面の評価値を計算する
long double calc_eval_01(const vector<vector<char>> &grid) {
    long double eval = 0;
    // 福（'o'）が落ちた場合、評価値から大きく減点する
    eval -= 1e9L * (2 * N - count_o(grid));
    // 鬼（'x'）が落ちた場合、評価値に加点する
    eval += 1e5L * (2 * N - count_x(grid));
    // 各 'x' について、落ちるまでの距離のM乗の逆数を加算する
    for (int i = 0; i < N; i++){
        for (int j = 0; j < N; j++){
            if (grid[i][j] == 'x')
                eval += calc_x_eval(grid, i, j);
        }
    }
    return eval;
}
 
// 貪欲法で操作を探索する再帰関数
// ans_list に操作 (方向, 位置) を追加していく
void search_01(const vector<vector<char>> &grid, vector<pair<char,int>> &ans_list) {
    long double max_eval = -1e18L;
    vector<vector<char>> best_grid;
    pair<char,int> best_move = {' ', 0};
    vector<char> directions = {'L', 'R', 'U', 'D'};
    // すべての行または列に対して、4方向の動作を試す
    for (char d : directions) {
        for (int p = 0; p < N; p++){
            auto new_grid = moveGrid(grid, d, p);
            long double curEval = calc_eval_01(new_grid);
            if (curEval > max_eval) {
                max_eval = curEval;
                best_grid = new_grid;
                best_move = {d, p};
            }
        }
    }
    ans_list.push_back(best_move);
    // もしすべての鬼が落ちたか、操作回数が 4*N^2 に達していたら終了
    if (count_x(best_grid) == 0 || ans_list.size() == (size_t)(4 * N * N))
        return;
    search_01(best_grid, ans_list);
}
 
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
 
    int n;
    cin >> n;  // 問題では20固定ですが、入力として読み込む
    vector<vector<char>> grid(N, vector<char>(N, '.'));
    for (int i = 0; i < N; i++){
        string s;
        cin >> s;
        for (int j = 0; j < N; j++){
            grid[i][j] = s[j];
        }
    }
 
    vector<pair<char,int>> ans_list;
    search_01(grid, ans_list);
 
    // 各操作を出力（方向と位置）
    for (auto &mv : ans_list) {
        cout << mv.first << " " << mv.second << "\n";
    }
 
    return 0;
}
