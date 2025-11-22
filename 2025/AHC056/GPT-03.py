# Python 3
# AHC: Grid Turing Robot - run-compression (reuse same (c,q) when A and D match)
# - Q=1（自己ループ）で内部状態を圧縮
# - 逆順に (D, next_color) をキーに色を再利用 ⇒ 連続区間で同一キーなら同じ (c,q)

import sys
from collections import deque, defaultdict

def read_input():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    N = int(next(it)); K = int(next(it)); T = int(next(it))
    v = [list(next(it).strip()) for _ in range(N)]        # N 行, 各 N-1
    h = [list(next(it).strip()) for _ in range(N-1)]      # N-1 行, 各 N
    targets = [(int(next(it)), int(next(it))) for _ in range(K)]
    return N, K, T, v, h, targets

def build_neighbors(N, v, h):
    neigh = [[[] for _ in range(N)] for __ in range(N)]
    for i in range(N):
        for j in range(N):
            if i > 0 and h[i-1][j] == '0':
                neigh[i][j].append((i-1, j))  # Up
            if i < N-1 and h[i][j] == '0':
                neigh[i][j].append((i+1, j))  # Down
            if j > 0 and v[i][j-1] == '0':
                neigh[i][j].append((i, j-1))  # Left
            if j < N-1 and v[i][j] == '0':
                neigh[i][j].append((i, j+1))  # Right
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
                path = [(di, dj)]
                ci, cj = di, dj
                while not (ci == si and cj == sj):
                    pi, pj = prev_i[ci][cj], prev_j[ci][cj]
                    path.append((pi, pj))
                    ci, cj = pi, pj
                path.reverse()
                return path
            q.append((ni, nj))
    # 連結は保証されているが、万一のフォールバック
    return [src, dst]

def dir_char(a, b):
    (i, j) = a
    (ni, nj) = b
    if ni == i-1 and nj == j: return 'U'
    if ni == i+1 and nj == j: return 'D'
    if ni == i and nj == j-1: return 'L'
    if ni == i and nj == j+1: return 'R'
    return 'S'

def main():
    N, K, T, v, h, targets = read_input()
    neigh = build_neighbors(N, v, h)

    # 目的地間を逐次 BFS 最短で繋ぐ（合計最短移動回数 X）
    route = [targets[0]]
    for i in range(K-1):
        path = bfs_path(N, neigh, targets[i], targets[i+1])
        if len(path) >= 2:
            route.extend(path[1:])
        else:
            route.extend(path)
    S = max(0, len(route) - 1)
    if S > T:
        route = route[:T+1]
        S = T

    # 各ステップの移動方向
    moves = []
    for t in range(S):
        moves.append(dir_char(route[t], route[t+1]))

    # 各マスを「起点として」訪れる時刻列 → 次の起点訪問時刻 nv[t]
    visits = defaultdict(list)
    for t in range(S):
        visits[route[t]].append(t)
    next_visit = [-1]*S
    for pos, lst in visits.items():
        for k in range(len(lst)-1):
            t = lst[k]
            next_visit[t] = lst[k+1]

    # 逆順に色を割り当て：キー (D, next_color)
    # - next_color = 0（以後このマスを起点で再訪しない）または color[nv]
    color_of_step = [0]*S       # ct[t] (>=1)
    key_to_color = {}           # (dir, next_color) -> color_id (>=1)
    color_rules = {}            # color_id -> (A, S=0, D)

    next_color_id = 1  # 1..C-1 を使用。0 は終端塗り専用
    for t in range(S-1, -1, -1):
        nv = next_visit[t]
        a = 0 if nv == -1 else color_of_step[nv]
        key = (moves[t], a)
        if key not in key_to_color:
            key_to_color[key] = next_color_id
            color_rules[next_color_id] = (a, '0', moves[t])  # S は 0 固定
            next_color_id += 1
        color_of_step[t] = key_to_color[key]

    C = next_color_id  # 使用色は 1..(C-1) + 0（終端専用）
    Q = 1              # 内部状態 1 種（常に 0）
    M = len(color_rules)

    # 初期色：各マスの最初の起点訪問時刻の色
    init_color = [[0]*N for _ in range(N)]
    seen = set()
    for t in range(S):
        i, j = route[t]
        if (i, j) not in seen:
            init_color[i][j] = color_of_step[t]
            seen.add((i, j))
    # 未訪問マスは 0 のまま（ルート上で踏まないため安全）

    # 出力
    print(C, Q, M)
    for i in range(N):
        print(' '.join(str(x) for x in init_color[i]))
    # ルールは色 1..C-1 のみ（色0は「終端に塗るだけ」で規則不要）
    for c in range(1, C):
        a, s, d = color_rules[c]
        # s は '0' 文字で良いが、他と合わせて整数 0 を出力
        print(c, 0, a, 0, d)

if __name__ == "__main__":
    main()
