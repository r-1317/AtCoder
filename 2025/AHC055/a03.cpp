#include <bits/stdc++.h>
using namespace std;

static constexpr int N = 200;

// weapon を使って box を攻撃し、状態を更新して出力文字列 "W B" を返す
string use_weapon(vector<int>& owned_weapons,
                  int weapon_index, int box_index,
                  vector<long long>& weapon_hp_list,
                  vector<long long>& box_hp_list,
                  const vector<vector<int>>& suitableness_matrix) {
    // 所持していない武器が指定された場合は素手にフォールバック（元コード準拠）
    if (weapon_index != -1) {
        bool has = false;
        for (int w : owned_weapons) if (w == weapon_index) { has = true; break; }
        if (!has) {
            // 素手攻撃
            int wi = N; // 素手の行
            long long attack_power = suitableness_matrix[wi][box_index];
            box_hp_list[box_index] -= attack_power;
            // 素手は耐久減少させない（させても問題ないが、十分大きいのでどちらでも可）
            if (box_hp_list[box_index] <= 0) {
                owned_weapons.push_back(box_index);
            }
            return to_string(-1) + " " + to_string(box_index);
        }
    }
    // 実際の攻撃処理
    int wi = (weapon_index == -1 ? N : weapon_index); // 素手は末尾行にマップ
    long long attack_power = suitableness_matrix[wi][box_index];
    box_hp_list[box_index] -= attack_power;

    if (weapon_index != -1) {
        weapon_hp_list[wi] -= 1;
    }
    // 宝箱が開いたらその箱の武器を入手
    if (box_hp_list[box_index] <= 0) {
        owned_weapons.push_back(box_index);
    }
    // 武器の耐久が尽きたら所持リストから削除（素手は除外）
    if (weapon_index != -1 && weapon_hp_list[wi] <= 0) {
        auto it = find(owned_weapons.begin(), owned_weapons.end(), weapon_index);
        if (it != owned_weapons.end()) owned_weapons.erase(it);
    }
    return to_string(weapon_index) + " " + to_string(box_index);
}

// 所持している武器の中から、最も効果的な攻撃ができる (box, weapon) を返す
pair<int,int> owned_best_pair(const vector<long long>& box_hp_list,
                              const vector<long long>& weapon_hp_list,
                              const vector<vector<int>>& suitableness_matrix,
                              const vector<int>& owned_weapons) {
    int best_box = -1;
    int best_weapon = -2; // -1 は素手を意味するため、-2 で初期化（元コード準拠）
    long long best_effective_power = -1;

    for (int box = 0; box < N; ++box) {
        if (box_hp_list[box] <= 0) continue; // 既に開いている
        for (int w : owned_weapons) {
            long long atk = suitableness_matrix[w][box];
            long long effective = min(atk, box_hp_list[box]);
            if (effective > best_effective_power) {
                best_effective_power = effective;
                best_box = box;
                best_weapon = w;
            }
        }
    }
    return {best_box, best_weapon};
}

// まだ開いていない宝箱の中から、最大攻撃力（全武器の中でその箱に対して最大）が最も大きい箱を返す
int never_opened_best_pair(const vector<long long>& box_hp_list,
                           const vector<vector<int>>& suitableness_matrix) {
    int best_box = -1;
    long long best_power = -1;
    for (int box = 0; box < N; ++box) {
        if (box_hp_list[box] <= 0) continue;
        long long mx = -1;
        for (int w = 0; w < N; ++w) { // 素手は含めない（元コード準拠）
            mx = max<long long>(mx, suitableness_matrix[w][box]);
        }
        if (mx > best_power) {
            best_power = mx;
            best_box = box;
        }
    }
    return best_box;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n_input;
    if (!(cin >> n_input)) return 0; // N は読み捨て（元コード準拠）

    vector<long long> box_hp_list(N);
    for (int i = 0; i < N; ++i) cin >> box_hp_list[i];

    vector<long long> weapon_hp_list(N + 1); // 末尾に素手
    for (int i = 0; i < N; ++i) cin >> weapon_hp_list[i];
    weapon_hp_list[N] = (long long)1e12; // 素手の「耐久」。実質無限

    vector<vector<int>> suitableness_matrix(N + 1, vector<int>(N));
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j)
            cin >> suitableness_matrix[i][j];
    // 素手の行を追加（全て 1）
    for (int j = 0; j < N; ++j) suitableness_matrix[N][j] = 1;

    vector<int> owned_weapons;
    int open_count = 0;

    // すべての宝箱が開くまで
    while (open_count < N) {
        int box_index, weapon_index;
        if (!owned_weapons.empty()) {
            auto p = owned_best_pair(box_hp_list, weapon_hp_list, suitableness_matrix, owned_weapons);
            box_index = p.first;
            weapon_index = p.second;
            // 念のためのフォールバック（全箱開封済みでなければ起きない想定）
            if (box_index == -1) {
                box_index = never_opened_best_pair(box_hp_list, suitableness_matrix);
                weapon_index = -1;
            }
        } else {
            box_index = never_opened_best_pair(box_hp_list, suitableness_matrix);
            weapon_index = -1; // 素手
        }

        string cmd = use_weapon(owned_weapons, weapon_index, box_index,
                                weapon_hp_list, box_hp_list, suitableness_matrix);
        cout << cmd << '\n';

        if (box_hp_list[box_index] <= 0) {
            ++open_count;
        }
    }
    return 0;
}
