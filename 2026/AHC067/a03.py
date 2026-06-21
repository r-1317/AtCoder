import sys
from collections import deque

sys.setrecursionlimit(10 ** 7)


def main():
    N, M, K = map(int, input().split())
    c = [input().strip() for _ in range(N)]

    # switch 0..8 を通常の関門用に使い、
    # switch 9 は設置せず、door 19 を永久閉鎖扉として使う。
    WALL_SWITCH = K - 1
    WALL_G = 2 * WALL_SWITCH + 1
    MAX_GATE_TYPES = K - 1

    # 永久壁用に少し扉枚数を残す。
    RESERVED_WALL_DOORS = 12
    GATE_DOOR_BUDGET = max(1, M - RESERVED_WALL_DOORS)

    # ----------------------------
    # 空きマスグラフ化
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

    # edge_g[eid] = -1 なら扉なし、そうでなければ扉型
    edge_g = [-1] * E

    # switch_by_v[v] = -1 ならスイッチなし、そうでなければ種類
    switch_by_v = [-1] * V

    # ----------------------------
    # BFS utility
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

    # ----------------------------
    # 遠い 2 点をアンカーにする
    # ----------------------------
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
            "gate_sources",
            "kind",
        )

        def __init__(self, cut_edges, mask, options, progress, gate_sources, kind):
            self.cut_edges = tuple(sorted(cut_edges))
            self.mask = mask
            self.side_count = mask.bit_count()
            self.options = options
            self.cost = len(cut_edges)
            self.progress = progress
            self.gate_sources = gate_sources
            self.kind = kind

    candidates = []
    seen_cuts = set()

    def make_candidate(cut_edges, kind):
        banned = set(cut_edges)

        # cut_edges を閉じたときの start 側成分
        dist_side = bfs_from(s_id, banned_edges=banned)

        # goal がまだ到達可能なら s-t カットではない
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

        # start 側成分内で、関門端点への距離を求める
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

            # start -> switch -> gate の遠回り量
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
            gate_sources=gate_sources,
            kind=kind,
        )

    def add_candidate(cut_edges, kind):
        if not cut_edges:
            return
        if len(cut_edges) > GATE_DOOR_BUDGET:
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
    # dist <= d の領域と、それより奥を分ける辺を同じ型で閉じる。
    # これにより、自然に「帯」を作りやすい。
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

    start_mask = 1 << s_id

    def transition_gain(prev_mask, cand):
        """
        prev_mask と cand.mask の差分帯にスイッチを置けるかを調べ、
        置けるなら最大 gain を返す。
        """
        band = cand.mask & ~prev_mask

        if band == 0:
            return None

        for gain, v in cand.options:
            if (band >> v) & 1:
                return gain

        return None

    # ----------------------------
    # ネストしたカット列を DP で選ぶ
    # ----------------------------
    #
    # 重要:
    #   スイッチは cand.mask 全体ではなく、
    #   prev_mask と cand.mask の差分帯に置く。
    #
    # これにより、未来のスイッチを手前でまとめて押されるのを抑える。
    # ----------------------------
    states = {(-1, 0, 0): (0, tuple())}
    # key = (last_candidate_index, used_gate_count, used_door_count)
    # value = (score, path)

    for cnt in range(MAX_GATE_TYPES):
        current_states = [
            (key, val) for key, val in states.items() if key[1] == cnt
        ]

        for (last, used_cnt, used_cost), (score, path) in current_states:
            if last == -1:
                prev_mask = start_mask
                prev_progress = -1
            else:
                prev_mask = candidates[last].mask
                prev_progress = candidates[last].progress

            used_edges = set()
            for idx in path:
                used_edges.update(candidates[idx].cut_edges)

            for ni, cand in enumerate(candidates):
                if ni in path:
                    continue

                if cand.progress <= prev_progress:
                    continue

                # ネスト条件: prev_mask ⊆ cand.mask
                if prev_mask & ~cand.mask:
                    continue

                if cand.mask == prev_mask:
                    continue

                if used_edges.intersection(cand.cut_edges):
                    continue

                new_cost = used_cost + cand.cost

                if new_cost > GATE_DOOR_BUDGET:
                    continue

                gain = transition_gain(prev_mask, cand)

                if gain is None:
                    continue

                # gain を重視しつつ、関門数もある程度評価する。
                add_score = gain * 5 + 25 - cand.cost * 3
                new_score = score + add_score
                new_key = (ni, used_cnt + 1, new_cost)
                new_path = path + (ni,)

                if new_key not in states or states[new_key][0] < new_score:
                    states[new_key] = (new_score, new_path)

    best_path = tuple()
    best_value = -10 ** 18

    for (last, used_cnt, used_cost), (score, path) in states.items():
        if used_cnt == 0:
            continue

        # 少しだけ関門数を優遇
        value = score + used_cnt * 20 - used_cost

        if value > best_value:
            best_value = value
            best_path = path

    if not best_path:
        print(0)
        print(0)
        return

    # ----------------------------
    # スイッチ位置を選ぶ
    # ----------------------------
    #
    # 各関門のスイッチは、
    #   前の関門の start 側成分との差分帯
    # に置く。
    #
    # さらに、遠い 2 点 a, b に交互に寄せる。
    # ----------------------------
    selected = []
    occupied_switch = set()
    prev_mask = start_mask
    prev_sw = -1
    used_gate_edges = set()

    def choose_switch(cand, step, prev_mask, prev_sw):
        band = cand.mask & ~prev_mask

        if band == 0:
            return None

        if step % 2 == 0:
            anchor_dist = dist_a
        else:
            anchor_dist = dist_b

        if prev_sw != -1:
            dist_prev_sw = bfs_from(prev_sw)
        else:
            dist_prev_sw = None

        best_score = -10 ** 18
        best_v = -1
        best_gain = -1

        for gain, v in cand.options:
            if ((band >> v) & 1) == 0:
                continue

            if v in occupied_switch:
                continue

            score = gain * 10

            # 交互に遠い側へ寄せる
            if anchor_dist[v] != -1:
                score -= anchor_dist[v] * 2

            # 直前のスイッチから遠いほど高評価
            if dist_prev_sw is not None and dist_prev_sw[v] != -1:
                score += dist_prev_sw[v] * 4

            if score > best_score:
                best_score = score
                best_v = v
                best_gain = gain

        if best_v == -1:
            return None

        return best_v, best_gain

    for idx in best_path:
        if len(selected) >= MAX_GATE_TYPES:
            break

        cand = candidates[idx]

        if used_gate_edges.intersection(cand.cut_edges):
            continue

        if prev_mask & ~cand.mask:
            continue

        res = choose_switch(cand, len(selected), prev_mask, prev_sw)

        if res is None:
            continue

        sw_v, _ = res

        selected.append((cand, sw_v))
        occupied_switch.add(sw_v)
        used_gate_edges.update(cand.cut_edges)
        prev_mask = cand.mask
        prev_sw = sw_v

    if not selected:
        print(0)
        print(0)
        return

    # ----------------------------
    # 扉・スイッチを実配置
    # ----------------------------
    door_output = []
    switch_output = []

    for k, (cand, sw_v) in enumerate(selected):
        g = 2 * k + 1

        for eid in cand.cut_edges:
            edge_g[eid] = g
            u, v, d, i, j = edges[eid]
            door_output.append((d, i, j, g))

        switch_by_v[sw_v] = k
        si, sj = cells[sw_v]
        switch_output.append((si, sj, k))

    # ----------------------------
    # 状態 BFS による評価
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

                path_edges = []
                cur = state

                while cur != start_state:
                    pe = parent_edge[cur]

                    if pe >= 0:
                        path_edges.append(pe)

                    cur = parent[cur]

                path_edges.reverse()
                return d0, path_edges

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

    initial_T = calc_T(False)

    if initial_T == 0:
        print(0)
        print(0)
        return

    # ----------------------------
    # 保護経路を作る
    # ----------------------------
    #
    # 永久壁を置くとき、想定攻略経路を壊しすぎないために、
    #   start -> switch -> gate -> switch -> gate -> ... -> goal
    # の 1 本の経路を保護する。
    # ----------------------------
    def shortest_path_edges_plain(src, dst, allowed_mask=None):
        if allowed_mask is not None:
            if ((allowed_mask >> src) & 1) == 0:
                return []
            if ((allowed_mask >> dst) & 1) == 0:
                return []

        par_v = [-1] * V
        par_e = [-1] * V

        q = deque([src])
        par_v[src] = src

        while q:
            v = q.popleft()

            if v == dst:
                break

            for to, eid in adj[v]:
                if allowed_mask is not None and ((allowed_mask >> to) & 1) == 0:
                    continue

                if par_v[to] == -1:
                    par_v[to] = v
                    par_e[to] = eid
                    q.append(to)

        if par_v[dst] == -1:
            return []

        res = []
        cur = dst

        while cur != src:
            res.append(par_e[cur])
            cur = par_v[cur]

        res.reverse()
        return res

    protected_edges = set()
    cur_v = s_id

    for cand, sw_v in selected:
        # switch までは cand.mask 内を通る想定
        p1 = shortest_path_edges_plain(cur_v, sw_v, cand.mask)
        protected_edges.update(p1)

        # switch から関門手前端点へ
        best_gate = None
        best_len = 10 ** 9
        best_inside = -1
        best_outside = -1

        dist_sw = bfs_from(sw_v, allowed_mask=cand.mask)

        for eid in cand.cut_edges:
            u, v, _, _, _ = edges[eid]
            u_in = (cand.mask >> u) & 1
            v_in = (cand.mask >> v) & 1

            if u_in and not v_in:
                inside, outside = u, v
            elif v_in and not u_in:
                inside, outside = v, u
            else:
                continue

            if dist_sw[inside] != -1 and dist_sw[inside] < best_len:
                best_len = dist_sw[inside]
                best_gate = eid
                best_inside = inside
                best_outside = outside

        if best_gate is not None:
            p2 = shortest_path_edges_plain(sw_v, best_inside, cand.mask)
            protected_edges.update(p2)
            protected_edges.add(best_gate)
            cur_v = best_outside

    p3 = shortest_path_edges_plain(cur_v, t_id, None)
    protected_edges.update(p3)

    gate_edges = set()
    for cand, _ in selected:
        gate_edges.update(cand.cut_edges)

    # ----------------------------
    # 永久閉鎖扉による横入り防止
    # ----------------------------
    #
    # door 19 は switch 9 に対応するが、switch 9 は置かない。
    # よって door 19 は初期状態から永久に閉じた壁として機能する。
    #
    # 現在の最短経路上にある、保護経路でない辺を試しに閉じ、
    # T が悪化せず、到達不能にもならないなら採用する。
    # ----------------------------
    def edge_to_output(eid, g):
        u, v, d, i, j = edges[eid]
        return d, i, j, g

    wall_trials = 0
    MAX_WALL_TRIALS = 80

    # スイッチ同士の直接経路も候補に入れる
    switch_vertices = [sw_v for _, sw_v in selected]
    switch_pair_edges = []

    for i in range(len(switch_vertices) - 1):
        path = shortest_path_edges_plain(switch_vertices[i], switch_vertices[i + 1])
        switch_pair_edges.extend(path)

    current_T = initial_T

    while len(door_output) < M and wall_trials < MAX_WALL_TRIALS:
        T_now, path_edges = calc_T(True)

        if T_now == 0:
            break

        current_T = T_now

        priority = []
        seen = set()

        # まず実際の最短経路上の辺を狙う
        for eid in path_edges:
            if eid not in seen:
                seen.add(eid)
                priority.append(eid)

        # 次に、連続するスイッチ間の短絡路を狙う
        for eid in switch_pair_edges:
            if eid not in seen:
                seen.add(eid)
                priority.append(eid)

        # それでも足りない場合、全辺も少し見る
        for eid in range(E):
            if eid not in seen:
                seen.add(eid)
                priority.append(eid)

        accepted = False

        for eid in priority:
            if wall_trials >= MAX_WALL_TRIALS:
                break

            if edge_g[eid] != -1:
                continue

            if eid in protected_edges:
                continue

            if eid in gate_edges:
                continue

            wall_trials += 1

            # 試しに永久壁を置く
            edge_g[eid] = WALL_G
            T2 = calc_T(False)

            if T2 != 0 and T2 >= current_T:
                door_output.append(edge_to_output(eid, WALL_G))
                current_T = T2
                accepted = True
                break
            else:
                edge_g[eid] = -1

        if not accepted:
            break

    # 最終検証
    final_T = calc_T(False)

    if final_T == 0:
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