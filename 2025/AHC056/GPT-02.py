# Python 3
# AHC: Grid Turing Robot - heuristic solver
# 方針: 各ステップを (c, q) に一意対応させ、最短経路で全目的地を巡回
# C×Q >= S を満たしつつ C+Q を最小化（おおよそ 2*sqrt(S)）

import sys
from collections import deque, defaultdict
import math

def read_input():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    N = int(next(it)); K = int(next(it)); T = int(next(it))
    # v: N 行, 各行 N-1 文字
    v = [list(next(it).strip()) for _ in range(N)]
    # h: N-1 行, 各行 N 文字
    h = [list(next(it).strip()) for _ in range(N-1)]
    targets = [(int(next(it)), int(next(it))) for _ in range(K)]
    return N, K, T, v, h, targets

def build_neighbors(N, v, h):
    # 各マスの近傍（壁を考慮）
    neigh = [[[] for _ in range(N)] for __ in range(N)]
    for i in range(N):
        for j in range(N):
            # Up
            if i > 0 and h[i-1][j] == '0':
                neigh[i][j].append((i-1, j))
            # Down
            if i < N-1 and h[i][j] == '0':
                neigh[i][j].append((i+1, j))
            # Left
            if j > 0 and v[i][j-1] == '0':
                neigh[i][j].append((i, j-1))
            # Right
            if j < N-1 and v[i][j] == '0':
                neigh[i][j].append((i, j+1))
    return neigh

def bfs_path(N, neigh, src, dst):
    if src == dst:
        return [src]
    si, sj = src
    di, dj = dst
    prev_i = [[-1]*N for _ in range(N)]
    prev_j = [[-1]*N for _ in range(N)]
    q = deque()
    q.append((si, sj))
    prev_i[si][sj] = si
    prev_j[si][sj] = sj
    while q:
        i, j = q.popleft()
        for ni, nj in neigh[i][j]:
            if prev_i[ni][nj] != -1:
                continue
            prev_i[ni][nj] = i
            prev_j[ni][nj] = j
            if (ni, nj) == (di, dj):
                # reconstruct
                path = [(di, dj)]
                ci, cj = di, dj
                while not (ci == si and cj == sj):
                    pi, pj = prev_i[ci][cj], prev_j[ci][cj]
                    path.append((pi, pj))
                    ci, cj = pi, pj
                path.reverse()
                return path
            q.append((ni, nj))
    # 連結は保証されているはず
    return [src, dst]  # フォールバック

def dir_char(a, b):
    (i, j) = a
    (ni, nj) = b
    if ni == i-1 and nj == j: return 'U'
    if ni == i+1 and nj == j: return 'D'
    if ni == i and nj == j-1: return 'L'
    if ni == i and nj == j+1: return 'R'
    return 'S'  # 通らないはず

def choose_CQ(S):
    if S <= 0:
        return 1, 1
    r = int(math.sqrt(S))
    best = (10**18, 1, S)  # (C+Q, Q, C)
    # 最適は sqrt(S) 付近にあるので、余裕をもって探索
    lo = max(1, r - 200)
    hi = r + 200
    for Q in range(lo, hi+1):
        C = (S + Q - 1) // Q
        val = C + Q
        if val < best[0]:
            best = (val, Q, C)
    # 念のため Q=1..min(S, 400) でも探索（S が極小の時のケア）
    limit = min(S, 400)
    for Q in range(1, limit+1):
        C = (S + Q - 1) // Q
        val = C + Q
        if val < best[0]:
            best = (val, Q, C)
    _, Q, C = best
    return C, Q

def main():
    N, K, T, v, h, targets = read_input()
    neigh = build_neighbors(N, v, h)

    # 全区間の最短経路を連結
    route = [targets[0]]
    for i in range(K-1):
        path = bfs_path(N, neigh, targets[i], targets[i+1])
        if len(path) >= 2:
            route.extend(path[1:])
        else:
            route.extend(path)

    S = max(0, len(route) - 1)  # 総ステップ数 = 最小移動回数 X
    # 念のため T ガード
    if S > T:
        # 仕様上起きないはずだが、安全にトリム（訪問未達になる）
        route = route[:T+1]
        S = T

    # C, Q を自動調整（C×Q >= S, C+Q 最小）
    C, Q = choose_CQ(S)

    # ステップ t に対して (c_t, q_t) を割り当て
    # q_t = t % Q, c_t = t // Q
    def ct(t): return t // Q
    def qt(t): return t % Q

    # 各ステップの移動方向
    moves = []
    for t in range(S):
        d = dir_char(route[t], route[t+1])
        moves.append(d)

    # 各マスを「原点（=出発側）」として訪れる時刻列
    visits = defaultdict(list)
    for t in range(S):
        visits[route[t]].append(t)

    # 次に同じマスを原点として訪れる時刻
    next_visit = [-1] * S
    for pos, lst in visits.items():
        for k in range(len(lst)-1):
            t = lst[k]
            next_visit[t] = lst[k+1]

    # 盤面初期色（初回訪問の c に合わせる）
    init_color = [[0]*N for _ in range(N)]
    seen_first = set()
    for t in range(S):
        i, j = route[t]
        if (i, j) not in seen_first:
            init_color[i][j] = ct(t)
            seen_first.add((i, j))
    # 未訪問マスは 0 のままで OK

    # 遷移規則 M 行を生成（各ステップに 1 行）
    # (c_t, q_t) は重複しない設計
    rules = []
    for t in range(S):
        c = ct(t)
        q = qt(t)
        dch = moves[t]
        nv = next_visit[t]
        if nv != -1:
            a = ct(nv)
        else:
            a = 0  # 次回訪問なし
        ns = (q + 1) % Q
        rules.append((c, q, a, ns, dch))

    # 出力
    M = len(rules)
    print(C, Q, M)
    for i in range(N):
        print(' '.join(str(x) for x in init_color[i]))
    for c, q, a, s, dch in rules:
        print(c, q, a, s, dch)

if __name__ == "__main__":
    main()
