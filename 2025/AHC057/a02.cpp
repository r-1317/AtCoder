#include <bits/stdc++.h>
using namespace std;

const int SIZE_LIMIT = 2;  // この大きさ以上の連結成分はM個までしか作らない

struct UnionFind {
    vector<int> parent_list;
    vector<int> size_list;

    UnionFind(int n) {
        parent_list.assign(n, -1);
        size_list.assign(n, 1);
    }

    int root(int x) {
        if (parent_list[x] == -1) return x;
        return parent_list[x] = root(parent_list[x]); // パス圧縮
    }

    bool is_same(int x, int y) {
        return root(x) == root(y);
    }

    void unite(int x, int y) {
        int rx = root(x);
        int ry = root(y);
        if (rx == ry) return;

        if (size_list[rx] < size_list[ry]) swap(rx, ry);
        parent_list[ry] = rx;
        size_list[rx] += size_list[ry];
        size_list[ry] = 0;
    }

    int size(int x) {
        return size_list[root(x)];
    }
};

// 指定した時間における、指定した点の座標を返す関数
pair<double, double> move_single_point(
    const vector<array<double, 2>>& point_coords,
    const vector<array<double, 2>>& velocities,
    UnionFind& uf,
    int current_time,
    int time,
    int point_id,
    int L
) {
    double x = point_coords[point_id][0];
    double y = point_coords[point_id][1];
    int r = uf.root(point_id);
    double vx = velocities[r][0];
    double vy = velocities[r][1];

    double dt = static_cast<double>(time - current_time);

    double current_x = x + vx * dt;
    double current_y = y + vy * dt;

    current_x = fmod(current_x, (double)L);
    if (current_x < 0) current_x += L;
    current_y = fmod(current_y, (double)L);
    if (current_y < 0) current_y += L;

    return {current_x, current_y};
}

// 2点間の距離を返す関数（トーラス考慮）
double distance_between_points(
    const pair<double, double>& p1,
    const pair<double, double>& p2,
    int L
) {
    double dx = fabs(p1.first - p2.first);
    double dy = fabs(p1.second - p2.second);
    dx = min(dx, (double)L - dx);
    dy = min(dy, (double)L - dy);
    double dist = sqrt(dx * dx + dy * dy);
    return dist;
}

// 指定した時間における、すべての点の座標を更新する関数
void move_all_points(
    vector<array<double, 2>>& point_coords,
    const vector<array<double, 2>>& velocities,
    UnionFind& uf,
    int current_time,
    int time,
    int L
) {
    int N = (int)point_coords.size();
    double dt = static_cast<double>(time - current_time);
    for (int i = 0; i < N; i++) {
        int r = uf.root(i);
        double vx = velocities[r][0];
        double vy = velocities[r][1];
        double x = point_coords[i][0];
        double y = point_coords[i][1];

        double current_x = x + vx * dt;
        double current_y = y + vy * dt;

        current_x = fmod(current_x, (double)L);
        if (current_x < 0) current_x += L;
        current_y = fmod(current_y, (double)L);
        if (current_y < 0) current_y += L;

        point_coords[i][0] = current_x;
        point_coords[i][1] = current_y;
    }
}

// 指定した時間における、指定した点に最も近い num_points 個の点のインデックスを返す関数
vector<int> get_nearest_points_at_time(
    const vector<array<double, 2>>& point_coords,
    const vector<array<double, 2>>& velocities,
    UnionFind& uf,
    int current_time,
    int time,
    int point_id,
    int num_points,
    int L,
    int K,
    int M,
    int large_components_count
) {
    int N = (int)point_coords.size();
    auto cur = move_single_point(point_coords, velocities, uf, current_time, time, point_id, L);
    double current_x = cur.first;
    double current_y = cur.second;

    vector<pair<double, int>> distances; // (距離, インデックス)

    for (int i = 0; i < N; i++) {
        if (i == point_id) continue;
        if (uf.is_same(point_id, i)) continue;
        if (uf.size(point_id) + uf.size(i) > K) continue;
        if (uf.size(point_id) < SIZE_LIMIT &&
            uf.size(i) < SIZE_LIMIT &&
            uf.size(point_id) + uf.size(i) >= SIZE_LIMIT &&
            large_components_count >= M) {
            continue;
        }

        auto cur2 = move_single_point(point_coords, velocities, uf, current_time, time, i, L);
        double distance = distance_between_points(
            {current_x, current_y},
            {cur2.first, cur2.second},
            L
        );
        distances.emplace_back(distance, i);
    }

    sort(distances.begin(), distances.end());
    vector<int> nearest_points;
    int limit = min(num_points, (int)distances.size());
    for (int i = 0; i < limit; i++) {
        nearest_points.push_back(distances[i].second);
    }
    return nearest_points;
}

// 指定した2点を結合し、そのときの距離を返す関数
double connect_points(
    UnionFind& uf,
    const vector<array<double, 2>>& point_coords,
    vector<array<double, 2>>& velocities,
    int point_id_1,
    int point_id_2,
    int K,
    int L
) {
    if (uf.size(point_id_1) + uf.size(point_id_2) > K) {
        // 結合しない（本来はここに来ない想定）
        return 0.0;
    }
    if (uf.is_same(point_id_1, point_id_2)) {
        // すでに同じ連結成分
        cerr << "Already connected" << endl;
        return 0.0;
    }

    double x1 = point_coords[point_id_1][0];
    double y1 = point_coords[point_id_1][1];
    double x2 = point_coords[point_id_2][0];
    double y2 = point_coords[point_id_2][1];

    double dist = distance_between_points({x1, y1}, {x2, y2}, L);

    // 速度ベクトルの更新（質量保存の法則）
    int size1 = uf.size(point_id_1);
    int size2 = uf.size(point_id_2);

    // 元コードでは velocities[point_id_1 / 2] を直接参照しているので、それに合わせる
    double vx_new =
        (velocities[point_id_1][0] * size1 + velocities[point_id_2][0] * size2)
        / (size1 + size2);
    double vy_new =
        (velocities[point_id_1][1] * size1 + velocities[point_id_2][1] * size2)
        / (size1 + size2);

    uf.unite(point_id_1, point_id_2);
    int root = uf.root(point_id_1);
    velocities[root][0] = vx_new;
    velocities[root][1] = vy_new;

    return dist;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, T, M, K, L;
    if (!(cin >> N >> T >> M >> K >> L)) {
        return 0;
    }

    UnionFind uf(N);
    vector<array<double, 2>> point_coords(N);   // [x, y]
    vector<array<double, 2>> velocities(N);     // [vx, vy]

    for (int i = 0; i < N; i++) {
        double x, y, vx, vy;
        cin >> x >> y >> vx >> vy;
        point_coords[i][0] = x;
        point_coords[i][1] = y;
        velocities[i][0] = vx;
        velocities[i][1] = vy;
    }

    int current_time = 0;
    int large_components_count = 0;
    double sum_cost = 0.0;

    // 3クロックごとに連結成分を増やす戦略
    for (int iter = 0; iter < (K - 1) * M; iter++) {
        double min_distance = 1e100;
        int point_id_1 = -1;
        int point_id_2 = -1;

        for (int j = 0; j < N; j++) {
            auto nearest_points = get_nearest_points_at_time(
                point_coords, velocities, uf,
                current_time, current_time,
                j, 1, L, K, M, large_components_count
            );
            for (int np : nearest_points) {
                double distance = distance_between_points(
                    {point_coords[j][0], point_coords[j][1]},
                    {point_coords[np][0], point_coords[np][1]},
                    L
                );
                if (distance < min_distance) {
                    min_distance = distance;
                    point_id_1 = j;
                    point_id_2 = np;
                }
            }
        }

        if (point_id_1 != -1 && point_id_2 != -1) {
            // SIZE_LIMIT以上の連結成分の数を更新
            int s1 = uf.size(point_id_1);
            int s2 = uf.size(point_id_2);
            if (s1 < SIZE_LIMIT && s2 < SIZE_LIMIT && s1 + s2 >= SIZE_LIMIT) {
                large_components_count += 1;
            } else if (s1 >= SIZE_LIMIT && s2 >= SIZE_LIMIT) {
                large_components_count -= 1;
            }

            sum_cost += connect_points(uf, point_coords, velocities, point_id_1, point_id_2, K, L);
            cout << current_time << " " << point_id_1 << " " << point_id_2 << "\n";
        } else {
            cerr << "No connectable points found" << endl;
        }

        // 3クロック進める
        move_all_points(point_coords, velocities, uf, current_time, current_time + 3, L);
        current_time += 3;
        if (current_time >= T) {
            cerr << "Reached time limit" << endl;
            break;
        }
    }

    // デバッグ出力
    cerr << "Total cost: " << sum_cost << "\n";
    vector<int> root_sizes;
    for (int i = 0; i < N; i++) {
        if (uf.root(i) == i) {
            root_sizes.push_back(uf.size(i));
        }
    }
    cerr << "Final root sizes: ";
    for (int s : root_sizes) cerr << s << " ";
    cerr << "\n";

    return 0;
}
