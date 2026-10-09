import sys
from collections import deque


DIRS = ((-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R"))
MAX_HEIGHT = 7


def main():
  N, K = map(int, input().split())
  size = N * N
  board = [input().strip() for _ in range(N)]
  towers = [[] for _ in range(size)]
  nests = [-1] * K
  floor = [False] * size

  for i in range(N):
    for j, cell in enumerate(board[i]):
      v = i * N + j
      if cell == "#":
        continue
      floor[v] = True
      if "a" <= cell <= "l":
        towers[v].append(ord(cell) - ord("a"))
      elif "A" <= cell <= "L":
        nests[ord(cell) - ord("A")] = v

  # 床だけを通る直線ジャンプを、逆向きの探索にも使えるようにする。
  neighbors = [[] for _ in range(size)]
  outgoing_jumps = [[] for _ in range(size)]
  incoming_jumps = [[] for _ in range(size)]
  for v in range(size):
    if not floor[v]:
      continue
    i, j = divmod(v, N)
    for di, dj, direction in DIRS:
      for length in range(1, MAX_HEIGHT + 1):
        ni, nj = i + di * length, j + dj * length
        if not (0 <= ni < N and 0 <= nj < N):
          break
        u = ni * N + nj
        if not floor[u]:
          break
        outgoing_jumps[v].append((u, length))
        incoming_jumps[u].append((v, length))
        if length == 1:
          neighbors[v].append((u, direction))

  dist_to_nest = []
  toward_nest = []
  for root in nests:
    dist = [-1] * size
    toward = [-1] * size
    dist[root] = 0
    queue = deque([root])
    while queue:
      v = queue.popleft()
      for u, _ in neighbors[v]:
        if dist[u] < 0:
          dist[u] = dist[v] + 1
          toward[u] = v
          queue.append(u)
    dist_to_nest.append(dist)
    toward_nest.append(toward)

  answer = []
  remaining = sum(map(len, towers))

  def jump_search(targets, color, used):
    """同色を運ぶ際に下に残るスライムを踏み台にした最短経路。"""
    # 木に取り込んだ同色スライムだけを踏み台候補から除く。
    reach = [min(MAX_HEIGHT,
                 1 + len(tower) - (tower.count(color) if v in used else 0))
             for v, tower in enumerate(towers)]
    distance = [-1] * size
    next_step = [-1] * size
    queue = deque(targets)
    for v in queue:
      distance[v] = 0
    while queue:
      v = queue.popleft()
      for u, length in incoming_jumps[v]:
        if distance[u] < 0 and length <= reach[u]:
          distance[u] = distance[v] + 1
          next_step[u] = v
          queue.append(u)
    return distance, next_step

  def start_step(v, distance, next_step):
    """出発点の上の1匹は踏み台にできないので、初手を別に選ぶ。"""
    if distance[v] == 0:
      return 0, v
    best = (size + 1, -1)
    for u, length in outgoing_jumps[v]:
      if length <= len(towers[v]) and distance[u] >= 0:
        candidate = (distance[u] + 1, u)
        if candidate >= best:
          continue
        # 逆向き探索が出発点自身のスライムを踏み台としていた経路は使えない。
        cur = u
        while cur != v and next_step[cur] >= 0:
          cur = next_step[cur]
        if cur == v:
          continue
        best = candidate
    return best

  def direction_and_length(src, dst):
    si, sj = divmod(src, N)
    ti, tj = divmod(dst, N)
    if si == ti:
      return ("R", tj - sj) if tj > sj else ("L", sj - tj)
    return ("D", ti - si) if ti > si else ("U", si - ti)

  def move(src, dst, count):
    nonlocal remaining
    height = len(towers[src])
    k = height - count
    direction, length = direction_and_length(src, dst)
    assert 0 <= k < height and 1 <= length <= k + 1
    assert len(towers[dst]) + count <= MAX_HEIGHT
    i, j = divmod(src, N)
    answer.append((i, j, k, direction, length))

    moving = towers[src][k:]
    del towers[src][k:]
    towers[dst].extend(reversed(moving))
    for v in (src, dst):
      for color, nest in enumerate(nests):
        if v == nest:
          while towers[v] and towers[v][-1] == color:
            towers[v].pop()
            remaining -= 1
          break

  def make_room(v, avoid=-1):
    """満杯のマスから、空き枠までの経路に沿って1匹ずつ押し出す。"""
    if len(towers[v]) < MAX_HEIGHT:
      return
    hole = -1
    for excluded in (avoid, -1):
      previous = [-1] * size
      previous[v] = v
      if excluded >= 0 and excluded != v:
        previous[excluded] = excluded
      queue = deque([v])
      while queue and hole < 0:
        cur = queue.popleft()
        for nxt, _ in neighbors[cur]:
          if previous[nxt] >= 0:
            continue
          previous[nxt] = cur
          if len(towers[nxt]) < MAX_HEIGHT:
            hole = nxt
            break
          queue.append(nxt)
      if hole >= 0:
        break
    if hole < 0:
      raise RuntimeError("No room on the board")

    path = [hole]
    while path[-1] != v:
      path.append(previous[path[-1]])
    path.reverse()
    for index in range(len(path) - 2, -1, -1):
      move(path[index], path[index + 1], 1)

  def build_tree(color, seed):
    """最短の1匹を軸に、木までの経路が短い順に同色を合流させる。"""
    root = nests[color]
    parent = {root: root}
    nest_distance, toward = jump_search((root,), color, ())
    v = seed
    first = start_step(seed, nest_distance, toward)[1]
    while v != root:
      if first < 0:
        nxt = toward_nest[color][v]
      else:
        nxt = first if v == seed else toward[v]
      parent[v] = nxt
      v = nxt

    positions = [v for v in range(size) if color in towers[v]]
    while True:
      distance, next_to_tree = jump_search(parent, color, parent)
      candidates = []
      for v in positions:
        if v in parent:
          continue
        to_tree, first = start_step(v, distance, next_to_tree)
        to_nest, _ = start_step(v, nest_distance, toward)
        if to_tree < to_nest:
          candidates.append((to_tree, v, first))
      if not candidates:
        break
      # 木を伸ばすたびに最短距離が変わるため、1匹ずつ選び直す。
      _, start, first = min(candidates)
      v = start
      while v not in parent:
        nxt = first if v == start else next_to_tree[v]
        parent[v] = nxt
        v = nxt
    return parent

  def send_on_tree(v, color, parent):
    if v == nests[color]:
      return
    nxt = parent[v]
    while towers[v] and towers[v][-1] == color:
      height = len(towers[v])
      run = 1
      while run < height and towers[v][height - run - 1] == color:
        run += 1

      dst = nxt
      _, length = direction_and_length(v, dst)
      if height - length + 1 <= 0:
        # 踏み台の移動などで計画時のジャンプができなくなった場合。
        path = shortest_single_path(v, nests[color])
        if path is None:
          return_one(v)
        else:
          for index in range(len(path) - 1):
            move(path[index], path[index + 1], 1)
        continue

      if len(towers[dst]) == MAX_HEIGHT:
        make_room(dst, v)
        # 空きを作る間に出発点の塔も変わり得るので、上から調べ直す。
        continue
      count = min(run, MAX_HEIGHT - len(towers[dst]), height - length + 1)
      move(v, dst, count)

  def shortest_single_path(start, goal):
    """現在の塔を考慮し、上の1匹を運ぶ操作数最小の経路を探す。"""
    previous = {start: None}
    queue = deque([start])
    while queue and goal not in previous:
      v = queue.popleft()
      i, j = divmod(v, N)
      k = len(towers[v]) - (1 if v == start else 0)
      for di, dj, direction in DIRS:
        for length in range(1, k + 2):
          ni, nj = i + di * length, j + dj * length
          if not (0 <= ni < N and 0 <= nj < N):
            break
          u = ni * N + nj
          if not floor[u]:
            break
          if len(towers[u]) >= MAX_HEIGHT or u in previous:
            continue
          previous[u] = v
          queue.append(u)
    if goal not in previous:
      return None
    path = [goal]
    while path[-1] != start:
      path.append(previous[path[-1]])
    path.reverse()
    return path

  def return_one(preferred=-1):
    """木で帰巣が起きなかった場合も、上にいる1匹は確実に帰す。"""
    while True:
      if preferred >= 0 and towers[preferred]:
        start = preferred
      else:
        visible = [v for v in range(size) if towers[v]]
        start = max(visible, key=lambda v: dist_to_nest[towers[v][-1]][v])
      color = towers[start][-1]
      goal = nests[color]
      path = shortest_single_path(start, goal)
      if path is None:
        # 高さ7の塔が通路を塞いでいれば、そこから空き枠へ1匹押し出す。
        v = start
        while toward_nest[color][v] != -1:
          v = toward_nest[color][v]
          if len(towers[v]) == MAX_HEIGHT:
            make_room(v, start)
            break
        continue
      for index in range(len(path) - 1):
        src, dst = path[index], path[index + 1]
        move(src, dst, 1)
      return

  while remaining:
    seed = -1
    color = -1
    best = (size + 1, True)
    for c in range(K):
      distance, next_step = jump_search((nests[c],), c, ())
      for v, tower in enumerate(towers):
        if c in tower:
          steps, _ = start_step(v, distance, next_step)
          candidate = (steps, tower[-1] != c)
          if candidate < best:
            best = candidate
            seed, color = v, c
    # 最短のスライムが埋まっていれば、塔の上を先に帰して取り出す。
    if towers[seed][-1] != color:
      return_one(seed)
      continue
    before = remaining
    parent = build_tree(color, seed)

    depth = {nests[color]: 0}
    for v in parent:
      if v in depth:
        continue
      chain = []
      u = v
      while u not in depth:
        chain.append(u)
        u = parent[u]
      for u in reversed(chain):
        depth[u] = depth[parent[u]] + 1
    for v in sorted(parent, key=lambda v: depth[v], reverse=True):
      send_on_tree(v, color, parent)

    if remaining == before:
      return_one(seed)

  for step in answer:
    print(*step)
  print(f"score: {len(answer)}", file=sys.stderr)


if __name__ == "__main__":
  main()
