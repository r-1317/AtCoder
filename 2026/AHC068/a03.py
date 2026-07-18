from collections import deque
from heapq import nlargest
from math import log2
from typing import List, Tuple
import sys


N = 20
SIZE = N * N
Operation = Tuple[str, int, int, int, int]


def read_input() -> Tuple[List[int], List[List[bool]], List[List[bool]]]:
  _ = int(input())
  cards = []
  for _ in range(N):
    cards.extend(map(int, input().split()))

  v_walls = [[False] * (N - 1) for _ in range(N)]
  for r in range(N):
    wall_str = input()
    for c in range(N - 1):
      v_walls[r][c] = wall_str[c] == '1'

  h_walls = [[False] * N for _ in range(N - 1)]
  for r in range(N - 1):
    wall_str = input()
    for c in range(N):
      h_walls[r][c] = wall_str[c] == '1'

  return cards, v_walls, h_walls


def build_neighbors(v_walls: List[List[bool]], h_walls: List[List[bool]]) -> List[List[int]]:
  neighbors = [[] for _ in range(SIZE)]
  for r in range(N):
    for c in range(N):
      u = r * N + c
      if c + 1 < N and not v_walls[r][c]:
        neighbors[u].append(u + 1)
        neighbors[u + 1].append(u)
      if r + 1 < N and not h_walls[r][c]:
        neighbors[u].append(u + N)
        neighbors[u + N].append(u)
  return neighbors


def all_pairs_distances(neighbors: List[List[int]]) -> List[List[int]]:
  distances = []
  for start in range(SIZE):
    dist = [-1] * SIZE
    dist[start] = 0
    queue = deque([start])
    while queue:
      u = queue.popleft()
      for v in neighbors[u]:
        if dist[v] == -1:
          dist[v] = dist[u] + 1
          queue.append(v)
    distances.append(dist)
  return distances


def operation_pairs(op: Operation) -> List[Tuple[int, int]]:
  d, r, c, h, w = op
  pairs = []
  if d == 'H':
    half = w // 2
    for i in range(r, r + h):
      base = i * N + c
      for j in range(half):
        pairs.append((base + j, base + half + j))
  else:
    half = h // 2
    for i in range(half):
      upper = (r + i) * N + c
      lower = (r + half + i) * N + c
      for j in range(w):
        pairs.append((upper + j, lower + j))
  return pairs


def build_lane_operations(
    v_walls: List[List[bool]], h_walls: List[List[bool]]
) -> Tuple[List[Operation], List[List[Tuple[int, int]]], List[List[int]]]:
  """高さ1の横ジャンプと幅1の縦ジャンプを全て列挙する。"""
  operations: List[Operation] = []
  pair_operations: List[List[Tuple[int, int]]] = [[] for _ in range(SIZE)]
  containing_operations: List[List[int]] = [[] for _ in range(SIZE)]

  def add_operation(op: Operation) -> None:
    index = len(operations)
    operations.append(op)
    cells = set()
    for u, v in operation_pairs(op):
      pair_operations[u].append((index, v))
      pair_operations[v].append((index, u))
      cells.add(u)
      cells.add(v)
    for u in cells:
      containing_operations[u].append(index)

  for r in range(N):
    for half in range(1, N // 2 + 1):
      width = 2 * half
      for c in range(N - width + 1):
        if not any(v_walls[r][j] for j in range(c, c + width - 1)):
          add_operation(('H', r, c, 1, width))

  for c in range(N):
    for half in range(1, N // 2 + 1):
      height = 2 * half
      for r in range(N - height + 1):
        if not any(h_walls[i][c] for i in range(r, r + height - 1)):
          add_operation(('V', r, c, height, 1))

  return operations, pair_operations, containing_operations


def articulation_points(active: List[bool], neighbors: List[List[int]]) -> List[bool]:
  """active が誘導する連結グラフの関節点を求める。"""
  discovery = [-1] * SIZE
  low = [0] * SIZE
  parent = [-1] * SIZE
  articulation = [False] * SIZE
  timer = 0

  def dfs(u: int) -> None:
    nonlocal timer
    discovery[u] = low[u] = timer
    timer += 1
    children = 0
    for v in neighbors[u]:
      if not active[v]:
        continue
      if discovery[v] == -1:
        parent[v] = u
        children += 1
        dfs(v)
        low[u] = min(low[u], low[v])
        if parent[u] == -1:
          if children >= 2:
            articulation[u] = True
        elif low[v] >= discovery[u]:
          articulation[u] = True
      elif v != parent[u]:
        low[u] = min(low[u], discovery[v])

  start = next((u for u in range(SIZE) if active[u]), -1)
  if start != -1:
    dfs(start)
  return articulation


def is_geometric_boundary(u: int, active: List[bool]) -> bool:
  r, c = divmod(u, N)
  if r == 0 or r + 1 == N or c == 0 or c + 1 == N:
    return True
  return (not active[u - N] or not active[u + N]
          or not active[u - 1] or not active[u + 1])


def geometric_degree(u: int, active: List[bool]) -> int:
  r, c = divmod(u, N)
  degree = 0
  if r > 0 and active[u - N]:
    degree += 1
  if r + 1 < N and active[u + N]:
    degree += 1
  if c > 0 and active[u - 1]:
    degree += 1
  if c + 1 < N and active[u + 1]:
    degree += 1
  return degree


def macro_distances(
    target: int,
    active: List[bool],
    pair_operations: List[List[Tuple[int, int]]],
    inactive_count: List[int],
) -> List[int]:
  """1回の長方形操作で移れるマス間を辺とした距離。"""
  dist = [-1] * SIZE
  dist[target] = 0
  queue = deque([target])
  while queue:
    u = queue.popleft()
    next_dist = dist[u] + 1
    for operation_index, v in pair_operations[u]:
      if inactive_count[operation_index] == 0 and dist[v] == -1:
        # operation が active のみを含むので v も必ず active。
        dist[v] = next_dist
        queue.append(v)
  return dist


def pair_gain(
    u: int, v: int, cards: List[int], distances: List[List[int]]
) -> Tuple[int, int]:
  card_u = cards[u]
  card_v = cards[v]
  before_distance = distances[u][card_u] + distances[v][card_v]
  after_distance = distances[u][card_v] + distances[v][card_u]
  before_correct = int(card_u == u) + int(card_v == v)
  after_correct = int(card_v == u) + int(card_u == v)
  return before_distance - after_distance, after_correct - before_correct


def operation_gain(
    op: Operation, cards: List[int], distances: List[List[int]]
) -> Tuple[int, int]:
  distance_gain = 0
  correct_gain = 0
  for u, v in operation_pairs(op):
    dg, cg = pair_gain(u, v, cards, distances)
    distance_gain += dg
    correct_gain += cg
  return distance_gain, correct_gain


def horizontal_component(
    row: int, c: int, w: int, active: List[bool],
    v_walls: List[List[bool]], h_walls: List[List[bool]],
) -> Tuple[int, int]:
  def row_usable(r: int) -> bool:
    base = r * N
    return (all(active[base + j] for j in range(c, c + w))
            and not any(v_walls[r][j] for j in range(c, c + w - 1)))

  def boundary_usable(r: int) -> bool:
    return not any(h_walls[r][j] for j in range(c, c + w))

  low = row
  while low > 0 and row_usable(low - 1) and boundary_usable(low - 1):
    low -= 1
  high = row
  while high + 1 < N and row_usable(high + 1) and boundary_usable(high):
    high += 1
  return low, high


def vertical_component(
    column: int, r: int, h: int, active: List[bool],
    v_walls: List[List[bool]], h_walls: List[List[bool]],
) -> Tuple[int, int]:
  def column_usable(c: int) -> bool:
    return (all(active[i * N + c] for i in range(r, r + h))
            and not any(h_walls[i][c] for i in range(r, r + h - 1)))

  def boundary_usable(c: int) -> bool:
    return not any(v_walls[i][c] for i in range(r, r + h))

  low = column
  while low > 0 and column_usable(low - 1) and boundary_usable(low - 1):
    low -= 1
  high = column
  while high + 1 < N and column_usable(high + 1) and boundary_usable(high):
    high += 1
  return low, high


def best_interval_containing_origin(scores: List[int], origin: int) -> Tuple[int, int]:
  """origin を含み、scores の和が最大となる区間を返す。"""
  best_left = origin
  best_sum = 0
  current = 0
  for i in range(origin - 1, -1, -1):
    current += scores[i]
    if current > best_sum:
      best_sum = current
      best_left = i

  best_right = origin
  best_sum = 0
  current = 0
  for i in range(origin + 1, len(scores)):
    current += scores[i]
    if current > best_sum:
      best_sum = current
      best_right = i
  return best_left, best_right


def expanded_operations(
    base_op: Operation,
    source: int,
    active: List[bool],
    cards: List[int],
    distances: List[List[int]],
    v_walls: List[List[bool]],
    h_walls: List[List[bool]],
) -> List[Operation]:
  """同じジャンプを隣接する行または列にもまとめて適用する候補。"""
  d, r, c, h, w = base_op
  source_r, source_c = divmod(source, N)
  candidates = {base_op}

  if d == 'H':
    low, high = horizontal_component(
        source_r, c, w, active, v_walls, h_walls)
    scores = []
    half = w // 2
    for row in range(low, high + 1):
      score = 0
      base = row * N + c
      for j in range(half):
        dg, cg = pair_gain(base + j, base + half + j, cards, distances)
        score += 4 * dg + 3 * cg
      scores.append(score)
    origin = source_r - low
    left, right = best_interval_containing_origin(scores, origin)
    spans = [
        (low + left, low + right),
        (low, high),
        (low, source_r),
        (source_r, high),
    ]
    for top, bottom in spans:
      candidates.add(('H', top, c, bottom - top + 1, w))
  else:
    low, high = vertical_component(
        source_c, r, h, active, v_walls, h_walls)
    scores = []
    half = h // 2
    for column in range(low, high + 1):
      score = 0
      for i in range(half):
        u = (r + i) * N + column
        v = (r + half + i) * N + column
        dg, cg = pair_gain(u, v, cards, distances)
        score += 4 * dg + 3 * cg
      scores.append(score)
    origin = source_c - low
    left, right = best_interval_containing_origin(scores, origin)
    spans = [
        (low + left, low + right),
        (low, high),
        (low, source_c),
        (source_c, high),
    ]
    for left_column, right_column in spans:
      candidates.add(('V', r, left_column, h, right_column - left_column + 1))

  return list(candidates)


def cycle_count(cards: List[int]) -> int:
  visited = [False] * SIZE
  count = 0
  for start in range(SIZE):
    if visited[start]:
      continue
    count += 1
    u = start
    while not visited[u]:
      visited[u] = True
      u = cards[u]
  return count


def cycle_count_after(cards: List[int], op: Operation) -> int:
  next_cards = cards.copy()
  for u, v in operation_pairs(op):
    next_cards[u], next_cards[v] = next_cards[v], next_cards[u]
  return cycle_count(next_cards)


def choose_operation(
    source: int,
    source_distance: int,
    macro_dist: List[int],
    operations: List[Operation],
    pair_operations: List[List[Tuple[int, int]]],
    inactive_count: List[int],
    active: List[bool],
    cards: List[int],
    distances: List[List[int]],
    v_walls: List[List[bool]],
    h_walls: List[List[bool]],
) -> Operation:
  candidates = set()
  for operation_index, destination in pair_operations[source]:
    if (inactive_count[operation_index] == 0
        and macro_dist[destination] == source_distance - 1):
      base_op = operations[operation_index]
      candidates.update(expanded_operations(
          base_op, source, active, cards, distances, v_walls, h_walls))

  # 距離と正解数で候補を絞り、サイクル数は上位候補だけ厳密に調べる。
  ranked = []
  for op in candidates:
    distance_gain, correct_gain = operation_gain(op, cards, distances)
    rough_score = 4 * distance_gain + 3 * correct_gain
    ranked.append((rough_score, distance_gain, correct_gain, op))

  top = nlargest(12, ranked)
  current_cycles = cycle_count(cards)
  best_key = None
  best_op = None
  for rough_score, distance_gain, correct_gain, op in top:
    cycle_gain = cycle_count_after(cards, op) - current_cycles
    score = rough_score + 5 * cycle_gain
    area = op[3] * op[4]
    key = (score, distance_gain, correct_gain, area)
    if best_key is None or key > best_key:
      best_key = key
      best_op = op

  # 隣接交換もマクログラフに含まれるため、通常ここには到達しない。
  if best_op is None:
    raise RuntimeError("no operation decreases the macro distance")
  return best_op


def apply_operation(cards: List[int], positions: List[int], op: Operation) -> None:
  for u, v in operation_pairs(op):
    card_u = cards[u]
    card_v = cards[v]
    cards[u], cards[v] = card_v, card_u
    positions[card_u] = v
    positions[card_v] = u


def main() -> None:
  cards, v_walls, h_walls = read_input()
  neighbors = build_neighbors(v_walls, h_walls)
  distances = all_pairs_distances(neighbors)
  operations, pair_operations, containing_operations = build_lane_operations(
      v_walls, h_walls)

  positions = [0] * SIZE
  for position, card in enumerate(cards):
    positions[card] = position

  active = [True] * SIZE
  active_count = SIZE
  inactive_count = [0] * len(operations)
  answer: List[Operation] = []

  while active_count > 1:
    articulation = articulation_points(active, neighbors)
    removable = [
        u for u in range(SIZE)
        if active[u] and not articulation[u] and is_geometric_boundary(u, active)
    ]
    if not removable:
      removable = [u for u in range(SIZE) if active[u] and not articulation[u]]

    # 安そうな候補だけマクログラフ上の正確な距離を調べる。
    removable.sort(key=lambda u: (
        positions[u] != u,
        distances[positions[u]][u],
        geometric_degree(u, active),
    ))
    shortlist = removable[:6]

    selected_target = -1
    selected_dist = None
    selected_key = None
    for target in shortlist:
      macro_dist = macro_distances(
          target, active, pair_operations, inactive_count)
      cost = macro_dist[positions[target]]
      key = (
          cost,
          positions[target] != target,
          geometric_degree(target, active),
          distances[positions[target]][target],
      )
      if selected_key is None or key < selected_key:
        selected_key = key
        selected_target = target
        selected_dist = macro_dist

    target = selected_target
    macro_dist = selected_dist
    source = positions[target]
    while source != target:
      source_distance = macro_dist[source]
      op = choose_operation(
          source, source_distance, macro_dist,
          operations, pair_operations, inactive_count,
          active, cards, distances, v_walls, h_walls)
      apply_operation(cards, positions, op)
      answer.append(op)
      source = positions[target]

    active[target] = False
    active_count -= 1
    for operation_index in containing_operations[target]:
      inactive_count[operation_index] += 1

  for d, r, c, h, w in answer:
    print(d, r, c, h, w)

  errors = sum(position != card for position, card in enumerate(cards))
  if errors:
    score = SIZE - errors
  else:
    score = SIZE + round(1_000_000 * log2(100_000 / len(answer)))
  print(score, file=sys.stderr)


if __name__ == "__main__":
  sys.setrecursionlimit(10 ** 6)
  main()
