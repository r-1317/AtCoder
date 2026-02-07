import os
from collections import deque
from typing import Tuple, List, Dict
import random

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

random.seed(1317)

# 定数
N = 100
K = 10
T = 10000

# 方針01用の定数
CANDIDATE_C = 10

# 方針02用の定数
P = 0.1  # ランダムに選ぶ確率

def main():
  n_in, m_in, k_in, t_in = map(int, input().split())
  # AHCの仕様上は定数だが、入力側を正として扱う
  n = n_in
  m = m_in
  k = k_in
  t = t_in

  adj_list: List[List[int]] = [[] for _ in range(n)]  # 0-index
  for _ in range(m):
    a, b = map(int, input().split())
    adj_list[a].append(b)
    adj_list[b].append(a)
  
  # 座標は必ず N 行与えられる（使わなくても読み捨てる）
  coords: List[Tuple[int, int]] = []
  for _ in range(n):
    x, y = map(int, input().split())
    coords.append((x, y))

  # --- 方針01: 店同士の最短経路を全組に対して割り出す ---
  def bfs_tree(src: int) -> Tuple[List[int], List[int]]:
    dist = [-1] * n
    parent = [-1] * n
    q = deque([src])
    dist[src] = 0
    while q:
      v = q.popleft()
      for nv in adj_list[v]:
        if dist[nv] != -1:
          continue
        dist[nv] = dist[v] + 1
        parent[nv] = v
        q.append(nv)
    return dist, parent

  shop_dist: List[List[int]] = [[-1] * k for _ in range(k)]
  shop_paths: List[List[List[int]]] = [[[] for _ in range(k)] for _ in range(k)]

  for s in range(k):
    dist, parent = bfs_tree(s)
    for g in range(k):
      shop_dist[s][g] = dist[g]
      if s == g:
        shop_paths[s][g] = [s]
        continue
      # 経路復元 (s -> g)
      path_rev: List[int] = []
      cur = g
      while cur != -1:
        path_rev.append(cur)
        if cur == s:
          break
        cur = parent[cur]
      path_rev.reverse()
      shop_paths[s][g] = path_rev

  nearest_shops: List[List[int]] = []
  for s in range(k):
    candidates = [g for g in range(k) if g != s]
    candidates.sort(key=lambda g: (shop_dist[s][g], g))
    nearest_shops.append(candidates)

  # --- 方針01: 訪問順と経路評価(使用回数・長さ) ---
  used_count: Dict[Tuple[int, int], int] = {}
  delivered_lengths: List[set[int]] = [set() for _ in range(k)]
  visit_order: List[int] = [0]

  cur = 0
  prev = -1  # 直前の行動1の移動元
  cone_len = 0  # 現状は色変え無しなので 'W' の長さだけ管理
  outputs: List[int] = []

  def choose_next_shop(src_shop: int, forbidden_first: int) -> int | None:
    # 近い順C個から試し、ダメなら全体から探す
    for pool in (nearest_shops[src_shop][:CANDIDATE_C], nearest_shops[src_shop]):
      best = None
      best_key = None
      for g in pool:
        path = shop_paths[src_shop][g]
        if len(path) >= 2 and forbidden_first != -1 and path[1] == forbidden_first:
          continue
        # 経路評価: 使用回数 -> 長さ（短いほど良い）
        uc = used_count.get((src_shop, g), 0)
        key = (uc, shop_dist[src_shop][g], g)
        if best_key is None or key < best_key:
          best_key = key
          best = g
      if best is not None:
        return best
    return None

  # 最初のみ例外: 一番近い店へ
  first_target = nearest_shops[0][0] if nearest_shops[0] else None
  if first_target is None:
    return

  def step_move_to(nxt: int) -> None:
    nonlocal cur, prev, cone_len
    outputs.append(nxt)
    prev, cur = cur, nxt
    if cur < k:
      delivered_lengths[cur].add(cone_len)
      cone_len = 0
      visit_order.append(cur)
    else:
      cone_len += 1

  def follow_path(path: List[int]) -> None:
    # path は cur を先頭に含む想定
    for nxt in path[1:]:
      if len(outputs) >= t:
        return
      # 制限: 直前の移動元へ戻れない
      if prev != -1 and nxt == prev:
        return
      step_move_to(nxt)

  # まず1本目の経路を辿る
  used_count[(0, first_target)] = used_count.get((0, first_target), 0) + 1
  follow_path(shop_paths[0][first_target])

  # 以降は、店にいるタイミングで次の店を選んで移動
  while len(outputs) < t:
    if cur < k:
      nxt_shop = choose_next_shop(cur, prev)
      if nxt_shop is None:
        # 念のためのフォールバック: 隣接のうち戻れない頂点以外へ
        fallback = None
        for nv in adj_list[cur]:
          if prev == -1 or nv != prev:
            fallback = nv
            break
        if fallback is None:
          break
        step_move_to(fallback)
        continue
      used_count[(cur, nxt_shop)] = used_count.get((cur, nxt_shop), 0) + 1
      follow_path(shop_paths[cur][nxt_shop])
    else:
      # 木にいる場合: とりあえず近い店へ向かう（木→店もBFSしてないので、隣へ進むだけ）
      # ただし今回の運用では基本的に shop→shop の経路追従で木に留まり続けない想定
      fallback = None
      for nv in adj_list[cur]:
        if prev == -1 or nv != prev:
          fallback = nv
          break
      if fallback is None:
        break
      step_move_to(fallback)

  ic(type(outputs), len(outputs))

  # 出力
  count = 0
  is_red_list = [False] * N
  p = P  # ランダムに選ぶ確率。次第に下がっていく
  for v in outputs:
    print(v)
    if v >= K and not is_red_list[v] and random.random() < p:
      is_red_list[v] = True
      print(-1)
      count += 1
      p *= 0.95
    count += 1
    if count >= t:
      break

if __name__ == "__main__":
  main()