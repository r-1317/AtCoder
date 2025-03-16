#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
using namespace std;

const int N = 100;
const int L = 500000;

// シミュレーションを行い、コストを計算する関数
int simulate(const vector<vector<int>>& next_employee_list, const vector<int>& t_list) {
    vector<int> cleaning_count_list(N, 0); // 各社員の掃除回数
    int current_employee = 0;              // 今週掃除を行う社員
    int sim = 500000;                      // シミュレーションする週数

    for (int i = 0; i < sim; i++) {
        cleaning_count_list[current_employee]++;
        if (cleaning_count_list[current_employee] % 2 == 1) {
            current_employee = next_employee_list[current_employee][0];
        } else {
            current_employee = next_employee_list[current_employee][1];
        }
    }

    int cost = 0;
    // L/sim は 500000/500000 = 1 となるが、コードの流れをそのまま再現
    for (int i = 0; i < N; i++) {
        cost += abs(cleaning_count_list[i] * (L / sim) - t_list[i]);
    }
    return cost;
}

int main() {
    int n, l;
    cin >> n >> l;  // n: 社員数(100固定), l: 掃除を行う週数(500000固定)
    
    vector<int> t_list(n);
    for (int i = 0; i < n; i++) {
        cin >> t_list[i];
    }
    
    // t_listの値が大きい順に社員のインデックスをソート
    vector<int> sorted_employees(n);
    for (int i = 0; i < n; i++) {
        sorted_employees[i] = i;
    }
    sort(sorted_employees.begin(), sorted_employees.end(), [&t_list](int a, int b) {
        return t_list[a] > t_list[b];
    });
    
    // 各社員が掃除を担当した場合の次の社員リスト (2要素)
    vector<vector<int>> next_employee_list(n, vector<int>(2, 0));
    for (int i = 0; i < n; i++) {
        int idx = sorted_employees[i];
        int next = sorted_employees[(i + 1) % n];
        next_employee_list[idx][0] = next;
        next_employee_list[idx][1] = next;
    }
    
    int max_employee = sorted_employees[0];  // 掃除回数が最も多い社員
    int min_cost = 1000000000;                // 初期値: 10**9
    vector<vector<int>> best_next_employee_list = next_employee_list;  // 最良のnext_employee_list
    
    // x_startとdxの組み合わせでnext_employee_listの更新を試行
    for (int x_start = 20; x_start <= 50; x_start++) {
        for (int dx = 4; dx <= 16; dx++) {
            vector<vector<int>> tmp_next_employee_list = next_employee_list;  // deepcopy
            int current_index = 0;
            int x = x_start;
            while (current_index + x < n && x > 0) {
                current_index += x;
                tmp_next_employee_list[sorted_employees[current_index]][1] = max_employee;
                x -= dx;
            }
            int cost = simulate(tmp_next_employee_list, t_list);
            if (cost < min_cost) {
                min_cost = cost;
                best_next_employee_list = tmp_next_employee_list;
            }
        }
    }
    
    // best_next_employee_list を出力
    for (int i = 0; i < n; i++) {
        cout << best_next_employee_list[i][0] << " " << best_next_employee_list[i][1] << "\n";
    }
    
    return 0;
}
