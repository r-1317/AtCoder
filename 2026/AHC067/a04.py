import sys
from collections import deque

sys.setrecursionlimit(10 ** 7)


def main():
    N, M, K = map(int, input().split())
    c = [input().strip() for _ in range(N)]

    # switch K-1 は設置せず、door 2*(K-1)+1 を永久閉鎖扉として使う
    WALL_SWITCH = K - 1
    WALL_G = 2 * WALL_SWITCH + 1

    # 0..K-2 を通常のトグル関門に使う
    MAX_PAIR_TYPES = K - 1

    # 永久壁用の扉枚数を残す
    RESERVED_WALL_DOORS = 10
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

    edge_g = [-1] * E
    switch_by_v = [-1] * V

    def edge_mask_of(edge_list):
        m = 0
        for eid in edge_list:
            m |= 1 << eid
        return m

    # ----------------------------
    # BFS
    # ----------------------------
    def bfs_from(src, banned_edges=None, allowed_mask=None):
        if banned_edges is None:
            banned_edges = set()

        dist = [-1] * V

        if allowed_mask is not None and ((allowed_mask >> src) & 1) == 0:
            return dist

        dist[src] = 0
        q = deque([src])

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

    def multi_bfs(sources, allowed_mask):
        dist = [-1] * V
        q = deque()

        for s in sources:
            if ((allowed_mask >> s) & 1) == 0:
                continue

            if dist[s] == -1:
                dist[s] = 0
                q.append(s)

        while q:
            v = q.popleft()

            for to, eid in adj[v]:
                if ((allowed_mask >> to) & 1) == 0:
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
    # 盤面上の遠い 2 点をアンカーにする
    # スイッチ配置を A 側 / B 側に交互に寄せるために使う
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
    # s-t カット候補
    # ----------------------------
    class CutCandidate:
        __slots__ = (
            "cut_edges",
            "edge_mask",
            "mask",
            "side_count",
            "cost",
            "progress",
            "kind",
        )

        def __init__(self, cut_edges, mask, progress, kind):
            self.cut_edges = tuple(sorted(cut_edges))
            self.edge_mask = edge_mask_of(self.cut_edges)
            self.mask = mask
            self.side_count = mask.bit_count()
            self.cost = len(cut_edges)
            self.progress = progress
            self.kind = kind

    candidates = []
    seen_cuts = set()

    def make_cut_candidate(cut_edges, kind):
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

        progress = min(dist_side[x] for x in gate_sources)

        return CutCandidate(cut_edges, mask, progress, kind)

    def add_cut_candidate(cut_edges, kind):
        if not cut_edges:
            return

        if len(cut_edges) > GATE_DOOR_BUDGET:
            return

        key = tuple(sorted(cut_edges))

        if key in seen_cuts:
            return

        seen_cuts.add(key)

        cand = make_cut_candidate(list(key), kind)

        if cand is not None:
            candidates.append(cand)

    # 1. 橋カット
    for eid in bridges:
        add_cut_candidate([eid], "bridge")

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
            add_cut_candidate(cut, "layer")

    if not candidates:
        print(0)
        print(0)
        return

    candidates.sort(key=lambda x: (x.progress, x.cost, x.side_count))

    # ----------------------------
    # 二重関門ペアを作る
    # ----------------------------
    #
    # entry cut: 扉 2k     初期開き、押すと閉まる
    # exit  cut: 扉 2k+1   初期閉じ、押すと開く
    #
    # switch は entry と exit の間の帯に置く。
    # ----------------------------
    class PairCandidate:
        __slots__ = (
            "entry",
            "exit",
            "entry_idx",
            "exit_idx",
            "edge_mask",
            "cost",
            "band_mask",
            "options",
            "best_gain",
            "progress",
        )

        def __init__(
            self,
            entry,
            exit_,
            entry_idx,
            exit_idx,
            edge_mask,
            cost,
            band_mask,
            options,
        ):
            self.entry = entry
            self.exit = exit_
            self.entry_idx = entry_idx
            self.exit_idx = exit_idx
            self.edge_mask = edge_mask
            self.cost = cost
            self.band_mask = band_mask
            self.options = options
            self.best_gain = options[0][0]
            self.progress = exit_.progress

    def make_pair(i, j):
        entry = candidates[i]
        exit_ = candidates[j]

        if entry.progress >= exit_.progress:
            return None

        # entry.mask ⊂ exit.mask が必要
        if entry.mask & ~exit_.mask:
            return None

        if entry.mask == exit_.mask:
            return None

        if entry.edge_mask & exit_.edge_mask:
            return None

        band_mask = exit_.mask & ~entry.mask

        if band_mask == 0:
            return None

        # entry cut の奥側端点、つまり band 側端点
        entry_ports = []

        for eid in entry.cut_edges:
            u, v, _, _, _ = edges[eid]
            u_entry = (entry.mask >> u) & 1
            v_entry = (entry.mask >> v) & 1
            u_band = (band_mask >> u) & 1
            v_band = (band_mask >> v) & 1

            if u_entry and v_band:
                entry_ports.append(v)
            elif v_entry and u_band:
                entry_ports.append(u)

        if not entry_ports:
            return None

        # exit cut の手前側端点、つまり band 側端点
        exit_ports = []

        for eid in exit_.cut_edges:
            u, v, _, _, _ = edges[eid]
            u_exit_side = (exit_.mask >> u) & 1
            v_exit_side = (exit_.mask >> v) & 1
            u_band = (band_mask >> u) & 1
            v_band = (band_mask >> v) & 1

            if u_exit_side and u_band and not v_exit_side:
                exit_ports.append(u)
            elif v_exit_side and v_band and not u_exit_side:
                exit_ports.append(v)

        if not exit_ports:
            return None

        dist_entry = multi_bfs(entry_ports, band_mask)
        dist_exit = multi_bfs(exit_ports, band_mask)

        base = min((dist_entry[x] for x in exit_ports if dist_entry[x] != -1), default=-1)

        if base == -1:
            return None

        options = []

        for v in range(V):
            if ((band_mask >> v) & 1) == 0:
                continue

            if dist_entry[v] == -1 or dist_exit[v] == -1:
                continue

            # entry -> switch -> exit の遠回り量
            detour = dist_entry[v] + dist_exit[v] - base

            # スイッチ押下 1 手も評価
            gain = detour + 1

            options.append((gain, v))

        if not options:
            return None

        options.sort(reverse=True)

        cost = entry.cost + exit_.cost

        if cost > GATE_DOOR_BUDGET:
            return None

        return PairCandidate(
            entry=entry,
            exit_=exit_,
            entry_idx=i,
            exit_idx=j,
            edge_mask=entry.edge_mask | exit_.edge_mask,
            cost=cost,
            band_mask=band_mask,
            options=options[:60],
        )

    pairs = []

    C = len(candidates)

    for i in range(C):
        for j in range(C):
            p = make_pair(i, j)

            if p is not None:
                pairs.append(p)

    if not pairs:
        print(0)
        print(0)
        return

    # ----------------------------
    # ペア列をビームサーチで選ぶ
    # ----------------------------
    #
    # prev_exit_mask ⊆ next_entry_mask となるように選ぶ。
    # これで、関門が start -> goal 方向に並ぶ。
    # ----------------------------
    start_mask = 1 << s_id

    BEAM_WIDTH = 240

    # state:
    #   (score, path_tuple, last_mask, last_progress, used_cost, used_edge_mask)
    beam = [(0, tuple(), start_mask, -1, 0, 0)]
    best_state = None

    for depth in range(MAX_PAIR_TYPES):
        nxt = []

        for score, path, last_mask, last_progress, used_cost, used_edge_mask in beam:
            for pi, p in enumerate(pairs):
                if p.progress <= last_progress:
                    continue

                if last_mask & ~p.entry.mask:
                    continue

                if used_edge_mask & p.edge_mask:
                    continue

                new_cost = used_cost + p.cost

                if new_cost > GATE_DOOR_BUDGET:
                    continue

                # 大きい gain と関門数を評価しつつ、扉枚数を少し嫌う
                add_score = p.best_gain * 12 + 45 - p.cost * 8

                # entry と exit の間の帯が極端に狭いものを少し嫌う
                if p.band_mask.bit_count() < 4:
                    add_score -= 40

                new_state = (
                    score + add_score,
                    path + (pi,),
                    p.exit.mask,
                    p.progress,
                    new_cost,
                    used_edge_mask | p.edge_mask,
                )

                nxt.append(new_state)

                if best_state is None or new_state[0] + len(new_state[1]) * 80 > best_state[0] + len(best_state[1]) * 80:
                    best_state = new_state

        if not nxt:
            break

        nxt.sort(key=lambda x: x[0] + len(x[1]) * 80, reverse=True)
        beam = nxt[:BEAM_WIDTH]

    if best_state is None or not best_state[1]:
        print(0)
        print(0)
        return

    selected_pair_indices = best_state[1]

    # ----------------------------
    # スイッチ位置を選ぶ
    # ----------------------------
    #
    # スイッチを遠い 2 つのクラスタに交互に寄せる。
    # さらに、直前のスイッチから遠い位置を優先する。
    # ----------------------------
    selected = []
    occupied_switch = set()
    prev_sw = -1

    def choose_switch(pair, step, prev_sw):
        if step % 2 == 0:
            anchor_dist = dist_a
        else:
            anchor_dist = dist_b

        if prev_sw != -1:
            dist_prev = bfs_from(prev_sw)
        else:
            dist_prev = None

        best_score = -10 ** 18
        best_v = -1

        for gain, v in pair.options:
            if v in occupied_switch:
                continue

            score = gain * 20

            # 偶数番目は a 側、奇数番目は b 側へ寄せる
            if anchor_dist[v] != -1:
                score -= anchor_dist[v] * 3

            # 直前のスイッチから遠いほど高評価
            if dist_prev is not None and dist_prev[v] != -1:
                score += dist_prev[v] * 5

            # 入口や玉座そのものにスイッチが寄りすぎるのを少し嫌う
            score += min(dist_start[v], 80)

            if score > best_score:
                best_score = score
                best_v = v

        if best_v == -1:
            return None

        return best_v

    for pi in selected_pair_indices:
        if len(selected) >= MAX_PAIR_TYPES:
            break

        pair = pairs[pi]
        sw_v = choose_switch(pair, len(selected), prev_sw)

        if sw_v is None:
            continue

        selected.append((pair, sw_v))
        occupied_switch.add(sw_v)
        prev_sw = sw_v

    if not selected:
        print(0)
        print(0)
        return

    # ----------------------------
    # 扉・スイッチ配置
    # ----------------------------
    door_output = []
    switch_output = []

    used_edges = set()

    for k, (pair, sw_v) in enumerate(selected):
        if k >= MAX_PAIR_TYPES:
            break

        # entry: 初期開き、押すと閉じる
        g_entry = 2 * k

        # exit: 初期閉じ、押すと開く
        g_exit = 2 * k + 1

        ok = True

        for eid in pair.entry.cut_edges:
            if eid in used_edges:
                ok = False

        for eid in pair.exit.cut_edges:
            if eid in used_edges:
                ok = False

        if not ok:
            continue

        for eid in pair.entry.cut_edges:
            used_edges.add(eid)
            edge_g[eid] = g_entry
            u, v, d, i, j = edges[eid]
            door_output.append((d, i, j, g_entry))

        for eid in pair.exit.cut_edges:
            used_edges.add(eid)
            edge_g[eid] = g_exit
            u, v, d, i, j = edges[eid]
            door_output.append((d, i, j, g_exit))

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
    # 永久閉鎖扉でショートカットを塞ぐ
    # ----------------------------
    #
    # switch K-1 は置いていないので、
    # door 2*(K-1)+1 は永久に閉じた扉として使える。
    #
    # 現在の最短経路や、スイッチ間の短絡路を試しに塞ぎ、
    # T が悪化せず、到達不能にもならないものだけ採用する。
    # ----------------------------
    def shortest_path_edges_plain(src, dst):
        par_v = [-1] * V
        par_e = [-1] * V

        q = deque([src])
        par_v[src] = src

        while q:
            v = q.popleft()

            if v == dst:
                break

            for to, eid in adj[v]:
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

    switch_vertices = [sw_v for _, sw_v in selected]
    switch_pair_edges = []

    for i in range(len(switch_vertices) - 1):
        switch_pair_edges.extend(shortest_path_edges_plain(switch_vertices[i], switch_vertices[i + 1]))

    current_T = initial_T
    wall_trials = 0
    MAX_WALL_TRIALS = 100

    while len(door_output) < M and wall_trials < MAX_WALL_TRIALS:
        T_now, path_edges = calc_T(True)

        if T_now == 0:
            break

        current_T = T_now

        priority = []
        seen = set()

        # まず実際の最短経路上の辺を塞ぐ候補にする
        for eid in path_edges:
            if eid not in seen:
                seen.add(eid)
                priority.append(eid)

        # 次にスイッチ間の素の短絡路を塞ぐ
        for eid in switch_pair_edges:
            if eid not in seen:
                seen.add(eid)
                priority.append(eid)

        # 残りの辺も少し見る
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

            wall_trials += 1

            edge_g[eid] = WALL_G
            T2 = calc_T(False)

            if T2 != 0 and T2 >= current_T:
                u, v, d, i, j = edges[eid]
                door_output.append((d, i, j, WALL_G))
                current_T = T2
                accepted = True
                break
            else:
                edge_g[eid] = -1

        if not accepted:
            break

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