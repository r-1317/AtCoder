/*
[Original Python (verbatim) — required by AtCoder translation rules]
import os
import math
import itertools

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def d2e(dx, dy):
  gcd = math.gcd(dx, dy)  # 最大公約数
  # 最大公約数で割る
  ex = dx // gcd
  ey = dy // gcd
  # exが負ならば反転
  if ex < 0:
    ex = -ex
    ey = -ey
  # ex == 0 かつ ey < 0の場合も反転
  if ex == 0 and ey < 0:
    ex = -ex
    ey = -ey
  return (ex, ey)

def main():
  N = int(input())
  coord_list = [tuple(map(int, input().split())) for _ in range(N)]  # 点の座標

  edge_to_idx_dict = {}
  edge_count_list = []  # 辺の出現回数
  edge_list = [[] for _ in range(N*(N-1))]  # 辺iの両端の点の集合

  for (x1, y1), (x2, y2) in itertools.combinations(coord_list, 2):
    dx = x2 - x1
    dy = y2 - y1
    
    ex, ey = d2e(dx, dy)  # 辺の大きさと方向を正規化

    if MyPC and (ex, ey) == (0, 1):
      ic(x1, y1, x2, y2)

    if (ex, ey) not in edge_to_idx_dict:
      edge_to_idx_dict[(ex, ey)] = len(edge_count_list)
      edge_count_list.append(1)
    else:
      edge_count_list[edge_to_idx_dict[(ex, ey)]] += 1

    ic(edge_to_idx_dict[(ex, ey)])
    edge_list[edge_to_idx_dict[(ex, ey)]].append(((x1, y1), (x2, y2)))

  ic(edge_to_idx_dict)

  ic(edge_count_list)

  ans = 0

  for count in edge_count_list:
    ans += count * (count - 1) // 2

  parallelogram_count = 0

  # 平行四辺形の除外
  multi_edge_list = []
  for i in range(len(edge_count_list)):
    if edge_count_list[i] > 1:
      for ((x1, y1), (x2, y2)), ((x3, y3), (x4, y4)) in itertools.combinations(edge_list[i], 2):
        # 平行四辺形の条件を満たすかチェック
        dx1 = x3 - x1
        dy1 = y3 - y1
        dx2 = x4 - x2
        dy2 = y4 - y2
        ex1, ey1 = d2e(dx1, dy1)
        ex2, ey2 = d2e(dx2, dy2)
        if ex1 == ex2 and ey1 == ey2:
          parallelogram_count += 1
        dx3 = x4 - x1
        dy3 = y4 - y1
        dx4 = x3 - x2
        dy4 = y3 - y2
        ex3, ey3 = d2e(dx3, dy3)
        ex4, ey4 = d2e(dx4, dy4)
        if ex3 == ex4 and ey3 == ey4:
          parallelogram_count += 1

  parallelogram_count //= 2  # 平行四辺形は2回カウントされているので半分にする

  ans -= parallelogram_count

  print(ans)

if __name__ == "__main__":
  main()

[END Original Python]
*/

// FAILED: Python-specific debug library 'icecream' setup is not applicable; debug calls are treated as no-ops in this C++ translation.

#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using P  = pair<ll,ll>;
using Edge = pair<P,P>;

// (Utility) Extract basename from a path (used to mirror MyPC idea; not essential for logic)
static string basename_cpp(const string& path) {
    size_t pos1 = path.find_last_of("/\\");
    return (pos1 == string::npos) ? path : path.substr(pos1 + 1);
}

// Debug stub to mirror `ic(...)` calls in Python; does nothing.
template <class... Args>
inline void ic(Args&&...) {}

// Normalize direction vector (dx, dy) -> (ex, ey) as in Python d2e
static inline P d2e(ll dx, ll dy) {
    ll g = std::gcd(dx, dy);       // gcd is non-negative
    ll ex = dx / g;
    ll ey = dy / g;
    if (ex < 0) { ex = -ex; ey = -ey; }
    if (ex == 0 && ey < 0) { ex = -ex; ey = -ey; }
    return {ex, ey};
}

// Hash for pair<long long, long long> to use with unordered_map (keeps average O(1) like Python dict)
struct PairHash {
    size_t operator()(const P& p) const noexcept {
        uint64_t x = static_cast<uint64_t>(p.first);
        uint64_t y = static_cast<uint64_t>(p.second);
        auto splitmix64 = [](uint64_t z) {
            z += 0x9e3779b97f4a7c15ULL;
            z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
            z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
            return z ^ (z >> 31);
        };
        uint64_t h1 = splitmix64(x);
        uint64_t h2 = splitmix64(y);
        return static_cast<size_t>(h1 ^ (h2 + 0x9e3779b97f4a7c15ULL + (h1 << 6) + (h1 >> 2)));
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Mirror the Python MyPC check (debug only; no effect on algorithm)
    const bool MyPC = (basename_cpp(__FILE__) != string("Main.cpp"));

    int N;
    if (!(cin >> N)) return 0;
    vector<P> coord_list(N);
    for (int i = 0; i < N; ++i) {
        ll x, y;
        cin >> x >> y;
        coord_list[i] = {x, y};
    }

    unordered_map<P, int, PairHash> edge_to_idx_dict;
    vector<ll> edge_count_list;                 // 出現回数
    vector<vector<Edge>> edge_list;             // 辺iの両端の点の集合
    edge_list.resize(static_cast<size_t>(N) * (N - 1)); // same size as Python: N*(N-1)

    // itertools.combinations(coord_list, 2)
    for (int a = 0; a < N; ++a) {
        for (int b = a + 1; b < N; ++b) {
            ll x1 = coord_list[a].first;
            ll y1 = coord_list[a].second;
            ll x2 = coord_list[b].first;
            ll y2 = coord_list[b].second;

            ll dx = x2 - x1;
            ll dy = y2 - y1;

            P e = d2e(dx, dy); // normalized direction (ex, ey)
            ll ex = e.first, ey = e.second;

            if (MyPC && ex == 0 && ey == 1) {
                ic(x1, y1, x2, y2);
            }

            int idx;
            auto it = edge_to_idx_dict.find(e);
            if (it == edge_to_idx_dict.end()) {
                idx = (int)edge_count_list.size();
                edge_to_idx_dict.emplace(e, idx);
                edge_count_list.push_back(1);
            } else {
                idx = it->second;
                edge_count_list[idx] += 1;
            }

            ic(idx);
            edge_list[idx].push_back({{x1, y1}, {x2, y2}});
        }
    }

    ic((int)edge_to_idx_dict.size());
    ic(edge_count_list.size());

    long long ans = 0;
    for (ll count : edge_count_list) {
        ans += count * (count - 1) / 2;
    }

    long long parallelogram_count = 0;

    // 平行四辺形の除外
    // (multi_edge_list is unused in Python; we keep behavior identical without using it.)
    for (size_t i = 0; i < edge_count_list.size(); ++i) {
        if (edge_count_list[i] > 1) {
            const auto& vec = edge_list[i];
            const size_t M = vec.size();
            for (size_t u = 0; u < M; ++u) {
                for (size_t v = u + 1; v < M; ++v) {
                    const auto& e1 = vec[u];
                    const auto& e2 = vec[v];
                    ll x1 = e1.first.first,  y1 = e1.first.second;
                    ll x2 = e1.second.first, y2 = e1.second.second;
                    ll x3 = e2.first.first,  y3 = e2.first.second;
                    ll x4 = e2.second.first, y4 = e2.second.second;

                    // Check condition 1
                    ll dx1 = x3 - x1, dy1 = y3 - y1;
                    ll dx2 = x4 - x2, dy2 = y4 - y2;
                    P n1 = d2e(dx1, dy1);
                    P n2 = d2e(dx2, dy2);
                    if (n1 == n2) parallelogram_count += 1;

                    // Check condition 2
                    ll dx3 = x4 - x1, dy3 = y4 - y1;
                    ll dx4 = x3 - x2, dy4 = y3 - y2;
                    P n3 = d2e(dx3, dy3);
                    P n4 = d2e(dx4, dy4);
                    if (n3 == n4) parallelogram_count += 1;
                }
            }
        }
    }

    parallelogram_count /= 2;  // counted twice
    ans -= parallelogram_count;

    cout << ans << '\n';
    return 0;
}