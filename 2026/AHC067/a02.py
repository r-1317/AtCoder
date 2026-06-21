import sys
from collections import deque
sys.setrecursionlimit(10 ** 7)


def main():
    N, M, K = map(int, input().split())
    c = [input().strip() for _ in range(N)]

    # ----------------------------
    # 空きマスを頂点化
    # ----------------------------
    vid = [[-1] * N for _ in range(N)]
    cells = []
    for i in range(N):
        for j in range(N):
            if c[i][j] == '.':
                vid[i][j] = len(cells)
                cells.append((i, j))

    V = len(cells)
    s_id = vid[0][0]
    t_id = vid[N - 1][N - 1]

    edges = []
    adj = [[] for _ in range(V)]

    def add_edge(u, v, d, i, j):
        eid = len(edges)
        edges.append((u, v, d, i, j))
        adj[u].append((v, eid))
        adj[v].append((u, eid))

    for i in range(N):
        for j in range(N):
            if vid[i][j] == -1:
                continue
            u = vid[i][j]

            if i + 1 < N and vid[i + 1][j] != -1:
                v = vid[i + 1][j]
                add_edge(u, v, 0, i, j)

            if j + 1 < N and vid[i][j + 1] != -1:
                v = vid[i][j + 1]
                add_edge(u, v, 1, i, j)

    E = len(edges)

    # ----------------------------
    # BFS utility
    # ----------------------------
    def bfs_from(src, banned_edges=None, allowed=None):
        if banned_edges is None:
            banned_edges = set()

        dist = [-1] * V
        if allowed is not None and not allowed[src]:
            return dist

        q = deque([src])
        dist[src] = 0

        while q:
            v = q.popleft()
            for to, eid in adj[v]:
                if eid in banned_edges:
                    continue
                if allowed is not None and not allowed[to]:
                    continue
                if dist[to] == -1:
                    dist[to] = dist[v] + 1
                    q.append(to)

        return dist

    dist_start = bfs_from(s_id)
    base_shortest = dist_start[t_id]

    # ----------------------------
    # 橋を列挙
    # ----------------------------
    tin = [-1] * V
    low = [-1] * V
    bridges = []
    timer = 0

    def dfs_bridge(v, peid):
        nonlocal timer
        tin[v] = low[v] = timer
        timer += 1

        for to, eid in adj[v]:
            if eid == peid:
                continue
            if tin[to] != -1:
                low[v] = min(low[v], tin[to])
            else:
                dfs_bridge(to, eid)
                low[v] = min(low[v], low[to])
                if low[to] > tin[v]:
                    bridges.append(eid)

    dfs_bridge(s_id, -1)

    # ----------------------------
    # カット候補を作る
    # ----------------------------
    class Candidate:
        __slots__ = (
            "cut_edges",
            "side",
            "switch_options",
            "cost",
            "gain",
            "progress",
            "kind",
        )

        def __init__(self, cut_edges, side, switch_options, gain, progress, kind):
            self.cut_edges = tuple(sorted(cut_edges))
            self.side = side
            self.switch_options = switch_options
            self.cost = len(cut_edges)
            self.gain = gain
            self.progress = progress
            self.kind = kind

    def make_candidate(cut_edges, kind):
        banned = set(cut_edges)

        # cut_edges を閉じたときの start 側成分
        dist_side = bfs_from(s_id, banned_edges=banned)
        if dist_side[t_id] != -1:
            return None

        side = [d != -1 for d in dist_side]

        # カット辺の start 側端点を gate_sources にする
        gate_sources = []
        for eid in cut_edges:
            u, v, _, _, _ = edges[eid]
            if side[u] and not side[v]:
                gate_sources.append(u)
            elif side[v] and not side[u]:
                gate_sources.append(v)
            else:
                # きれいな s-t カットではない
                return None

        if not gate_sources:
            return None

        # start 側で gate_sources への距離
        allowed = side
        dist_gate = [-1] * V
        q = deque()
        for x in gate_sources:
            if dist_gate[x] == -1:
                dist_gate[x] = 0
                q.append(x)

        while q:
            v = q.popleft()
            for to, eid in adj[v]:
                if eid in banned:
                    continue
                if not allowed[to]:
                    continue
                if dist_gate[to] == -1:
                    dist_gate[to] = dist_gate[v] + 1
                    q.append(to)

        base_gate = min(dist_side[x] for x in gate_sources)

        options = []
        for v in range(V):
            if not side[v]:
                continue
            if dist_side[v] == -1 or dist_gate[v] == -1:
                continue

            # start -> switch -> gate の遠回り量
            detour = dist_side[v] + dist_gate[v] - base_gate
            gain = detour + 1  # スイッチを押す 1 手
            options.append((gain, v))

        if not options:
            return None

        options.sort(reverse=True)
        best_gain = options[0][0]
        progress = base_gate

        return Candidate(
            cut_edges=cut_edges,
            side=side,
            switch_options=options[:40],
            gain=best_gain,
            progress=progress,
            kind=kind,
        )

    candidates = []
    seen_cuts = set()

    def add_candidate(cut_edges, kind):
        if not cut_edges:
            return
        if len(cut_edges) > M:
            return

        key = tuple(sorted(cut_edges))
        if key in seen_cuts:
            return
        seen_cuts.add(key)

        cand = make_candidate(list(key), kind)
        if cand is not None:
            candidates.append(cand)

    # 1. 橋カット
    for eid in bridges:
        add_candidate([eid], "bridge")

    # 2. BFS 距離の等高線カット
    #
    # dist_start <= d の領域と、それより外側を分ける辺集合。
    # これを全部同じ型の閉じ扉にすると、必ず s-t カットになる。
    #
    # cut_size が大きすぎるものは扉を食いすぎるので除外。
    MAX_LAYER_CUT = 10

    if base_shortest != -1:
        for d in range(base_shortest):
            cut = []
            for eid, (u, v, _, _, _) in enumerate(edges):
                du = dist_start[u]
                dv = dist_start[v]
                if du == -1 or dv == -1:
                    continue
                if (du <= d < dv) or (dv <= d < du):
                    cut.append(eid)

            if 1 <= len(cut) <= MAX_LAYER_CUT:
                add_candidate(cut, "layer")

    # 候補がない場合は何も置かない
    if not candidates:
        print(0)
        print(0)
        return

    # ----------------------------
    # 候補を選ぶ
    # ----------------------------
    #
    # efficiency = 推定増加手数 / 扉枚数
    # ただし実際の攻略順が自然になるよう、最後は progress 昇順に並べる。
    #
    candidates.sort(key=lambda x: (-(x.gain / x.cost), -x.gain, x.cost))

    selected = []
    used_edges = set()
    used_doors = 0

    for cand in candidates:
        if len(selected) >= K:
            break
        if used_doors + cand.cost > M:
            continue
        if any(eid in used_edges for eid in cand.cut_edges):
            continue

        selected.append(cand)
        used_doors += cand.cost
        for eid in cand.cut_edges:
            used_edges.add(eid)

    # start -> goal 方向に並べる
    selected.sort(key=lambda x: x.progress)

    # ----------------------------
    # 扉・スイッチ配置を作る
    # ----------------------------
    door_h = [[-1] * N for _ in range(N - 1)]
    door_v = [[-1] * (N - 1) for _ in range(N)]
    switch = [[-1] * N for _ in range(N)]

    door_output = []
    switch_output = []

    occupied_switch_cell = set()

    actual_selected = []

    for k, cand in enumerate(selected):
        if k >= K:
            break

        # スイッチ位置を選ぶ。
        # 同じマスに複数置けないので、未使用の最良候補を採用。
        sw_v = -1
        for _, v in cand.switch_options:
            if v not in occupied_switch_cell:
                sw_v = v
                break

        if sw_v == -1:
            continue

        # 初期閉じ扉を使う: 型 2k+1
        g = 2 * k + 1

        ok = True
        local_doors = []

        for eid in cand.cut_edges:
            u, v, d, i, j = edges[eid]

            if d == 0:
                if door_h[i][j] != -1:
                    ok = False
                    break
                local_doors.append((d, i, j, g))
            else:
                if door_v[i][j] != -1:
                    ok = False
                    break
                local_doors.append((d, i, j, g))

        if not ok:
            continue

        for d, i, j, g in local_doors:
            if d == 0:
                door_h[i][j] = g
            else:
                door_v[i][j] = g
            door_output.append((d, i, j, g))

        si, sj = cells[sw_v]
        switch[si][sj] = k
        switch_output.append((si, sj, k))
        occupied_switch_cell.add(sw_v)
        actual_selected.append(cand)

    # ----------------------------
    # 最短行動回数を計算して検証
    # ----------------------------
    def calc_T():
        def is_open(g, mask):
            if g == -1:
                return True
            kk = g // 2
            return ((mask >> kk) & 1) == (g & 1)

        INF = -1
        dist = [[[-1] * N for _ in range(N)] for _ in range(1 << K)]
        dist[0][0][0] = 0

        q = deque()
        q.append((0, 0, 0))

        while q:
            mask, i, j = q.popleft()
            d0 = dist[mask][i][j]

            if i == N - 1 and j == N - 1:
                return d0

            # 移動
            for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                ni = i + di
                nj = j + dj

                if not (0 <= ni < N and 0 <= nj < N):
                    continue
                if c[ni][nj] == '#':
                    continue

                if di == 1:
                    g = door_h[i][j]
                elif di == -1:
                    g = door_h[ni][nj]
                elif dj == 1:
                    g = door_v[i][j]
                else:
                    g = door_v[ni][nj]

                if not is_open(g, mask):
                    continue

                if dist[mask][ni][nj] == -1:
                    dist[mask][ni][nj] = d0 + 1
                    q.append((mask, ni, nj))

            # スイッチ
            ssw = switch[i][j]
            if ssw != -1:
                nmask = mask ^ (1 << ssw)
                if dist[nmask][i][j] == -1:
                    dist[nmask][i][j] = d0 + 1
                    q.append((nmask, i, j))

        return 0

    T = calc_T()

    # 到達不能なら安全に何も置かない
    if T == 0:
        print(0)
        print(0)
        return

    # ----------------------------
    # 出力
    # ----------------------------
    print(len(door_output))
    for d, i, j, g in door_output:
        print(d, i, j, g)

    print(len(switch_output))
    for i, j, s in switch_output:
        print(i, j, s)


if __name__ == "__main__":
    main()