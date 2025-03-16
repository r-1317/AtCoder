#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>  // abs
using namespace std;

const int N = 100;
const int L = 500000;

int simulate(const vector<vector<int>> &next_employee_list, const vector<int> &t_list) {
    vector<int> cleaning_count_list(N, 0);
    int current_employee = 0;
    int sim = 500000;  // シミュレーションする週数

    for (int i = 0; i < sim; i++) {
        cleaning_count_list[current_employee]++;
        if (cleaning_count_list[current_employee] % 2 == 1) {
            current_employee = next_employee_list[current_employee][0];
        } else {
            current_employee = next_employee_list[current_employee][1];
        }
    }
    
    int cost = 0;
    // L/sim は 500000/500000 = 1 となる
    for (int i = 0; i < N; i++) {
        cost += abs(cleaning_count_list[i] * (L / sim) - t_list[i]);
    }
    
    return cost;
}

int main() {
    int n, l;
    cin >> n >> l;  // n: 社員数, l: 掃除を行う週数（lは以降使用しない）
    
    vector<int> t_list(n);
    for (int i = 0; i < n; i++) {
        cin >> t_list[i];
    }
    
    // t_listが大きい順に社員のインデックスをソート
    vector<int> sorted_employees(n);
    for (int i = 0; i < n; i++) {
        sorted_employees[i] = i;
    }
    sort(sorted_employees.begin(), sorted_employees.end(), [&](int a, int b) {
        return t_list[a] > t_list[b];
    });
    
    // 各社員の次に掃除を行う社員（[0]:掃除回数が奇数の場合、[1]:偶数の場合）
    vector<vector<int>> next_employee_list(n, vector<int>(2, 0));
    for (int i = 0; i < n; i++) {
        int next = sorted_employees[(i + 1) % n];
        next_employee_list[sorted_employees[i]][0] = next;
        next_employee_list[sorted_employees[i]][1] = next;
    }
    
    int max_employee = sorted_employees[0];
    
    // x人おきに、next_employee_listの2つ目の社員をmax_employeeに変更
    int x = 35;  // 初期値
    int dx = 8;  // 減少量
    int current_index = 0;
    while (current_index + x < n && x > 0) {
        current_index += x;
        next_employee_list[sorted_employees[current_index]][1] = max_employee;
        x -= dx;
    }
    
    // next_employee_listを出力
    for (int i = 0; i < n; i++) {
        cout << next_employee_list[i][0] << " " << next_employee_list[i][1] << "\n";
    }
    
    // cout << simulate(next_employee_list, t_list) << "\n";
    
    return 0;
}
