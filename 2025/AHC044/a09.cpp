#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <cmath>

using namespace std;
typedef long long ll;

const int SIM = 500000;  // シミュレーション週数

// シミュレーション関数
ll simulate(const vector<vector<int>>& next_employee_list, const vector<int>& t_list, int l) {
    int n = t_list.size();
    vector<int> cleaning_count(n, 0);
    int current_employee = 0;
    for (int i = 0; i < SIM; i++) {
        cleaning_count[current_employee]++;
        if (cleaning_count[current_employee] % 2 == 1) {
            current_employee = next_employee_list[current_employee][0];
        } else {
            current_employee = next_employee_list[current_employee][1];
        }
    }
    ll cost = 0;
    int factor = l / SIM;  // 整数除算
    for (int i = 0; i < n; i++) {
        cost += abs(cleaning_count[i] * factor - t_list[i]);
    }
    return cost;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, l;
    cin >> n >> l;
    vector<int> t_list(n);
    for (int i = 0; i < n; i++){
        cin >> t_list[i];
    }

    // 理想の掃除回数が多い順に社員のインデックスをソート
    vector<int> sorted_employees(n);
    for (int i = 0; i < n; i++){
        sorted_employees[i] = i;
    }
    sort(sorted_employees.begin(), sorted_employees.end(), [&t_list](int a, int b) {
        return t_list[a] > t_list[b];
    });

    // next_employee_listの初期化
    vector<vector<int>> next_employee_list(n, vector<int>(2, 0));
    for (int i = 0; i < n; i++){
        int idx = sorted_employees[i];
        int next_idx = sorted_employees[(i + 1) % n];
        next_employee_list[idx][0] = next_idx;
        next_employee_list[idx][1] = next_idx;
    }
    int max_employee = sorted_employees[0];

    ll min_cost = 1000000000LL;  // 十分大きな初期値
    vector<vector<int>> best_next_employee_list = next_employee_list;
    int best_x_start = 0, best_dx = 0;

    // x_startとdxの全探索
    for (int x_start = 20; x_start <= 50; x_start++){
        for (int dx = 4; dx <= 16; dx++){
            vector<vector<int>> tmp_next_employee_list = next_employee_list;
            int current_index = 0;
            int x = x_start;
            while (current_index + x < n && x > 0) {
                current_index += x;
                tmp_next_employee_list[sorted_employees[current_index]][1] = max_employee;
                x -= dx;
            }
            ll cost = simulate(tmp_next_employee_list, t_list, l);
            if (cost < min_cost) {
                min_cost = cost;
                best_next_employee_list = tmp_next_employee_list;
                best_x_start = x_start;
                best_dx = dx;
            }
        }
    }

    // 先頭に戻る場所のリストを作成
    vector<int> x_return_list;
    int current_index = 0;
    int x = best_x_start;
    while (current_index + x < n && x > 0) {
        current_index += x;
        x_return_list.push_back(current_index);
        x -= best_dx;
    }
    if (!x_return_list.empty() && x_return_list.back() == n - 1) {
        x_return_list.pop_back();
    }
    next_employee_list = best_next_employee_list;
    int m = x_return_list.size();
    int combinations = 1 << m;
    // 総当たりで調整
    for (int i = 0; i < combinations; i++){
        vector<vector<int>> tmp_next_employee_list = next_employee_list;
        for (int j = 0; j < m; j++){
            if (i & (1 << j)) {
                int idx = x_return_list[j];
                tmp_next_employee_list[idx][1] = tmp_next_employee_list[idx][0];
                if (idx + 1 < n) {
                    tmp_next_employee_list[idx + 1][1] = max_employee;
                }
            }
        }
        ll cost = simulate(tmp_next_employee_list, t_list, l);
        if (cost < min_cost) {
            min_cost = cost;
            best_next_employee_list = tmp_next_employee_list;
        }
    }

    // 結果を出力
    for (int i = 0; i < n; i++){
        cout << best_next_employee_list[i][0] << " " << best_next_employee_list[i][1] << "\n";
    }

    return 0;
}
