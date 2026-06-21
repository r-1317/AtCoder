import sys
from collections import deque

sys.setrecursionlimit(10 ** 7)


def main():
    N, M, K = map(int, input().split())
    c = [input().strip() for _ in range(N)]

    # 最後の bit は永久壁用に温存する。
    # switch 9 を置かなければ、door 19 は永久に閉じた扉として使える。
    WALL_SWITCH = K - 1
    WALL_G = 2 * WALL_SWITCH + 1

    MAX_GATE_TYPES = K - 1
    GATE_DOOR_BUDGET = 34

    # ----------------------------
    # 空きマスをグラフ化
    # ----------------------------
    vid = [[-1] * N for _ in range(N)]
    cells = []

    for i in range(N):
        for j in range(N):
            if c[i][j] == ".":
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
                add_edge(u, vid[i + 1][j], 0, i, j)

            if j + 1 < N and vid[i][j + 1] != -1:
                add_edge(u, vid[i][j + 1], 1, i, j)

    E = len(edges)

    # edge_g[eid] = -1 なら扉なし
    edge_g = [-1] * E

    # switch_by_v[v] = -1 ならスイッチなし
    switch_by_v = [-1] * V

    # ----------------------------
    # 通常 BFS
    # ----------------------------
    def bfs_from(src, banned_edges=None, allowed_mask=None):
        if banned_edges is None:
            banned_edges = set()

        dist = [-1] * V

        if allowed_mask is not None:
            if ((allowed_mask >> src) & 1) == 0:
                return dist

        q = deque([src])
        dist[src] = 0

        while q:
            v = q.popleft()

            for to, eid in adj[v]:
                if eid in banned_edges:
                    continue

                if allowed_mask is not None and ((allowed_mask >> to) & 1) == 0:
                    continue

                if dist[to] == -1:
                    dist[to] = dist[v] + 1
                    q.append(to)

        return dist

    dist_start = bfs_from(s_id)
    base_shortest = dist_start[t_id]

    if base_shortest == -1:
        print(0)
        print(0)
        return

    # 遠い 2 点をスイッチクラスタのアンカーにする
    a = max(range(V), key=lambda x: dist_start[x])
    dist_a = bfs_from(a)
    b = max(range(V), key=lambda x: dist_a[x])
    dist_b = bfs_from(b)

    # ----------------------------
    # 橋を列挙
    # ----------------------------
    tin = [-1] * V
    low = [-1] * V
    timer = 0
    bridges = []

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
    # 関門候補
    # ----------------------------
    class Candidate:
        __slots__ = (
            "cut_edges",
            "mask",
            "side_count",
            "options",
            "cost",
            "progress",
            "kind",
        )

        def __init__(self, cut_edges, mask, options, progress, kind):
            self.cut_edges = tuple(sorted(cut_edges))
            self.mask = mask
            self.side_count = mask.bit_count()
            self.options = options
            self.cost = len(cut_edges)
            self.progress = progress
            self.kind = kind

    candidates = []
    seen_cuts = set()

    def make_candidate(cut_edges, kind):
        banned = set(cut_edges)

        # cut_edges を閉じたときの start 側成分
        dist_side = bfs_from(s_id, banned_edges=banned)

        if dist_side[t_id] != -1:
            return None

        mask = 0
        for v in range(V):
            if dist_side[v] != -1:
                mask |= 1 << v

        gate_sources = []

        for eid in cut_edges:
            u, v, _, _, _ = edges[eid]

            u_in = (mask >> u) & 1
            v_in = (mask >> v) & 1

            if u_in and not v_in:
                gate_sources.append(u)
            elif v_in and not u_in:
                gate_sources.append(v)
            else:
                return None

        if not gate_sources:
            return None

        # start 側成分内で関門端点への距離
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

                if ((mask >> to) & 1) == 0:
                    continue

                if dist_gate[to] == -1:
                    dist_gate[to] = dist_gate[v] + 1
                    q.append(to)

        base_gate = min(dist_side[x] for x in gate_sources)

        options = []

        for v in range(V):
            if ((mask >> v) & 1) == 0:
                continue

            if dist_side[v] == -1 or dist_gate[v] == -1:
                continue

            detour = dist_side[v] + dist_gate[v] - base_gate
            gain = detour + 1
            options.append((gain, v))

        if not options:
            return None

        options.sort(reverse=True)

        return Candidate(
            cut_edges=cut_edges,
            mask=mask,
            options=options,
            progress=base_gate,
            kind=kind,
        )

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
    MAX_LAYER_CUT = 12

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

    if not candidates:
        print(0)
        print(0)
        return

    candidates.sort(key=lambda x: (x.side_count, x.progress, x.cost))

    def door_count():
        return sum(1 for g in edge_g if g != -1)

    # ----------------------------
    # 初期解: ネストした関門列を作る
    # ----------------------------
    selected = []
    occupied_switch = set()
    used_edges = set()

    prev_mask = 1 << s_id
    prev_sw = -1
    used_gate_doors = 0

    for step in range(MAX_GATE_TYPES):
        best = None

        if prev_sw != -1:
            dist_prev_sw = bfs_from(prev_sw)
        else:
            dist_prev_sw = None

        anchor_dist = dist_a if step % 2 == 0 else dist_b

        for ci, cand in enumerate(candidates):
            if prev_mask & ~cand.mask:
                continue

            if cand.mask == prev_mask:
                continue

            if used_edges.intersection(cand.cut_edges):
                continue

            if used_gate_doors + cand.cost > GATE_DOOR_BUDGET:
                continue

            band = cand.mask & ~prev_mask

            for gain, v in cand.options:
                if ((band >> v) & 1) == 0:
                    continue

                if v in occupied_switch:
                    continue

                score = gain * 10 - cand.cost * 20

                # 直前のスイッチから遠いほど良い
                if dist_prev_sw is not None and dist_prev_sw[v] != -1:
                    score += dist_prev_sw[v] * 4

                # 偶数番目/奇数番目で遠いクラスタに寄せる
                if anchor_dist[v] != -1:
                    score -= anchor_dist[v] * 2

                # 進みすぎる候補を少し抑える
                score -= cand.side_count // 8

                if best is None or score > best[0]:
                    best = (score, ci, v)

        if best is None:
            break

        _, ci, sw_v = best
        cand = candidates[ci]

        selected.append((cand, sw_v))
        occupied_switch.add(sw_v)
        used_edges.update(cand.cut_edges)
        used_gate_doors += cand.cost

        prev_mask = cand.mask
        prev_sw = sw_v

    if not selected:
        print(0)
        print(0)
        return

    # 初期解では、関門 k は switch k を押すと開く扉 2k+1
    for k, (cand, sw_v) in enumerate(selected):
        g = 2 * k + 1

        for eid in cand.cut_edges:
            edge_g[eid] = g

        switch_by_v[sw_v] = k

    used_switch_types = len(selected)

    # ----------------------------
    # 状態付き BFS
    # ----------------------------
    def is_open(g, mask):
        if g == -1:
            return True

        k = g // 2
        return ((mask >> k) & 1) == (g & 1)

    def calc_T(need_path=False):
        total_states = (1 << K) * V
        dist = [-1] * total_states

        if need_path:
            parent = [-1] * total_states
            parent_edge = [-3] * total_states
        else:
            parent = None
            parent_edge = None

        start_state = s_id
        dist[start_state] = 0

        q = deque([start_state])

        while q:
            state = q.popleft()
            mask = state // V
            v = state % V
            d0 = dist[state]

            if v == t_id:
                if not need_path:
                    return d0

                path = []
                cur = state

                while cur != start_state:
                    p = parent[cur]
                    e = parent_edge[cur]

                    if e >= 0:
                        pmask = p // V
                        path.append((pmask, e))

                    cur = p

                path.reverse()
                return d0, path

            # 移動
            for to, eid in adj[v]:
                g = edge_g[eid]

                if not is_open(g, mask):
                    continue

                ns = mask * V + to

                if dist[ns] == -1:
                    dist[ns] = d0 + 1

                    if need_path:
                        parent[ns] = state
                        parent_edge[ns] = eid

                    q.append(ns)

            # スイッチ
            sw = switch_by_v[v]

            if sw != -1:
                nmask = mask ^ (1 << sw)
                ns = nmask * V + v

                if dist[ns] == -1:
                    dist[ns] = d0 + 1

                    if need_path:
                        parent[ns] = state
                        parent_edge[ns] = -2

                    q.append(ns)

        if need_path:
            return 0, []

        return 0

    current_T = calc_T(False)

    if current_T == 0:
        print(0)
        print(0)
        return

    # ----------------------------
    # 改良 1:
    # スイッチの周囲を別 bit の状態で囲む
    # ----------------------------
    #
    # 例:
    #   switch 1 の隣接辺すべてに door 1 を置く
    #   => switch 0 が ON のときだけ switch 1 に入れる
    #
    #   switch 2 の隣接辺すべてに door 0 を置く
    #   => switch 0 が OFF のときだけ switch 2 に入れる
    #
    # calc_T で改善したものだけ採用する。
    # ----------------------------
    switch_vertices = [sw_v for _, sw_v in selected]

    def try_access_condition_gates(current_T):
        for target in range(1, used_switch_types):
            sw_v = switch_vertices[target]
            incident = [eid for _, eid in adj[sw_v]]

            # 全方向を同じ条件で囲める場合だけ試す。
            # 既に扉があると抜け道や重複が面倒なのでスキップする。
            if any(edge_g[eid] != -1 for eid in incident):
                continue

            if door_count() + len(incident) > M:
                continue

            best_T = current_T
            best_g = -1

            # 「前に登場したスイッチ」の状態を条件にする
            for ctrl in range(target):
                for val in (0, 1):
                    g = 2 * ctrl + val

                    for eid in incident:
                        edge_g[eid] = g

                    T2 = calc_T(False)

                    for eid in incident:
                        edge_g[eid] = -1

                    if T2 != 0 and T2 > best_T:
                        best_T = T2
                        best_g = g

            if best_g != -1:
                for eid in incident:
                    edge_g[eid] = best_g

                current_T = best_T

        return current_T

    current_T = try_access_condition_gates(current_T)

    # ----------------------------
    # 改良 2:
    # 現在の最短経路を見て、その mask では閉じる扉を追加する
    # ----------------------------
    #
    # path 上の移動辺 e を、通過時 mask で閉じる扉に変える。
    #
    # bit k が 1 のとき:
    #   door 2k は閉じている
    #   => switch k を押したことで閉まる扉
    #
    # bit k が 0 のとき:
    #   door 2k+1 は閉じている
    #   => switch k を押す必要がある扉
    #
    # どちらも試し、calc_T が増えたものだけ採用する。
    # ----------------------------
    def try_state_dependent_blockers(current_T):
        max_iters = min(18, M - door_count())
        max_trials_per_iter = 60

        for _ in range(max_iters):
            if door_count() >= M:
                break

            T_now, path = calc_T(True)

            if T_now == 0:
                break

            current_T = T_now

            cand_list = []
            seen = set()

            for pos, (mask, eid) in enumerate(path):
                if edge_g[eid] != -1:
                    continue

                # 既に同じ辺を候補に入れていたら軽く抑制するが、
                # g が違うものは試す価値がある。
                for k in range(used_switch_types):
                    bit = (mask >> k) & 1
                    val = bit ^ 1
                    g = 2 * k + val

                    key = (eid, g)
                    if key in seen:
                        continue
                    seen.add(key)

                    priority = pos

                    # bit=1 のとき door 2k を置くのは、
                    # 「押したことで閉まった扉」なので強く優先する。
                    if bit == 1 and val == 0:
                        priority += 10000

                    # 序盤より中盤以降のほうが状態差が効きやすい
                    priority += pos * 3

                    cand_list.append((priority, eid, g))

                # 永久壁候補
                # switch 9 は置いていないので、door 19 は永久閉鎖。
                if WALL_SWITCH >= used_switch_types:
                    g = WALL_G
                    key = (eid, g)

                    if key not in seen:
                        seen.add(key)
                        priority = pos + 100
                        cand_list.append((priority, eid, g))

            if not cand_list:
                break

            cand_list.sort(reverse=True)

            best_T = current_T
            best_move = None

            tried = 0

            for _, eid, g in cand_list:
                if tried >= max_trials_per_iter:
                    break

                if edge_g[eid] != -1:
                    continue

                tried += 1

                edge_g[eid] = g
                T2 = calc_T(False)
                edge_g[eid] = -1

                if T2 != 0 and T2 > best_T:
                    best_T = T2
                    best_move = (eid, g)

            if best_move is None:
                break

            eid, g = best_move
            edge_g[eid] = g
            current_T = best_T

        return current_T

    current_T = try_state_dependent_blockers(current_T)

    # 最終検証
    final_T = calc_T(False)

    if final_T == 0:
        print(0)
        print(0)
        return

    # ----------------------------
    # 出力
    # ----------------------------
    door_output = []

    for eid, g in enumerate(edge_g):
        if g == -1:
            continue

        _, _, d, i, j = edges[eid]
        door_output.append((d, i, j, g))

    switch_output = []

    for v, sw in enumerate(switch_by_v):
        if sw == -1:
            continue

        i, j = cells[v]
        switch_output.append((i, j, sw))

    print(len(door_output))
    for d, i, j, g in door_output:
        print(d, i, j, g)

    print(len(switch_output))
    for i, j, s in switch_output:
        print(i, j, s)


if __name__ == "__main__":
    main()