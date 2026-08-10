import os
from typing import Tuple, List
import math

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 50  # 固定
M = 1000  # 固定
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

K = 1.0  # 支払額の基準値を決める係数。1.0に設定しておく。

class GroupInfo:
  """
  グループ情報を保持するクラス(sample.pyから)
  ### 属性
  - s: 到着時刻
  - t: 退去時刻
  - p: 人数
  - v: 基本支払額
  - c: コンパクト度（配置後に設定）
  - pos: 占有マスの座標 [(行, 列), ...]（配置後に設定）
  """
  def __init__(self, s, t, p, v):
    self.s = s        # 到着時刻
    self.t = t        # 退去時刻
    self.p = p        # 人数
    self.v = v        # 基本支払額
    self.c = None     # コンパクト度（配置後に設定）
    self.pos = None   # 占有マスの座標 [(行, 列), ...]（配置後に設定）

def compactness(region: List[Tuple[int, int]], p: int) -> float:
  """
  コンパクト度を返す関数(sample.pyから)
  ### 入力
  - region: 占有マスの座標リスト [(行, 列), ...]
  - p: 人数
  ### 出力
  - コンパクト度（float）
  """
  cells = set(region)
  perimeter = 0
  for (x, y) in region:
    for dx, dy in DIRS:
      if (x + dx, y + dy) not in cells:
        perimeter += 1
  return 4 * math.sqrt(p) / perimeter

def expected_v(s: int, t: int, p: int) -> float:
  """
  支払額の期待値を返す関数
  ### 入力
  - s: 到着時刻
  - t: 退去時刻
  - p: 人数
  ### 出力
  - 支払額の期待値（float）
  """
  return p * (t - s)**0.9

def release_groups(groups: List[GroupInfo], owner: List[List[int]], current_time: int) -> int:
  """
  退去時刻が現在時刻より前のグループを解放
  ### 入力
  - groups: グループ情報のリスト
  - owner: 占有者のIDを保持するグリッド
  - current_time: 現在時刻
  ### 出力
  - 解放されたグループの支払額の合計（int）
  """
  released_money = 0
  for group in groups:
    if group.pos is None or group.t >= current_time:
      continue
    for x, y in group.pos:
      owner[x][y] = -1
    released_money += int(group.v * group.c + 0.5)
    group.pos = None
  return released_money

def find_best_placement(grid: List[List[int]], owner: List[List[int]], groups: List[GroupInfo], new_group: GroupInfo, R: float) -> Tuple[List[List[Tuple[int, int]]], List[Tuple[int, int]]]:
  """
  BFSでグループを配置する関数
  p個連続した空きマスがなかった場合、移動して配置することを考慮する。
  移動コストが支払額を上回る場合は、移動せず、配置もしない。
  ### 入力
  - grid: 芝生のグリッド
  - owner: 占有者のIDを保持するグリッド
  - groups: グループ情報のリスト
  - new_group: 新たに配置するグループ情報
  ### 出力
  - 移動するグループの座標リスト [[(行, 列), ...], ...]
    - 各グループの移動先の座標を保持するリスト。移動しない場合は空リスト。
  - 新たに配置するグループの占有マスの座標リスト [(行, 列), ...]
  """
  moves = [[] for _ in groups]

  def find_region(p: int, movable: int = -1, forbidden=None):
    visited = [[False] * N for _ in range(N)]
    for sx in range(N):
      for sy in range(N):
        if visited[sx][sy] or grid[sx][sy] or (owner[sx][sy] != -1 and owner[sx][sy] != movable):
          continue
        start = sx * N + sy
        if forbidden is not None and start in forbidden:
          continue
        visited[sx][sy] = True
        queue = [start]
        head = 0
        while head < len(queue) and len(queue) < p:
          cell = queue[head]
          head += 1
          x, y = divmod(cell, N)
          for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < N and 0 <= ny < N) or visited[nx][ny] or grid[nx][ny]:
              continue
            ncell = nx * N + ny
            if (forbidden is not None and ncell in forbidden) or (owner[nx][ny] != -1 and owner[nx][ny] != movable):
              continue
            visited[nx][ny] = True
            queue.append(ncell)
            if len(queue) == p:
              break
        if len(queue) >= p:
          return [divmod(cell, N) for cell in queue[:p]]
    return None

  # 移動しなくても置ける場合は、移動費を払わない。
  region = find_region(new_group.p)
  if region is not None:
    new_group.pos = region
    return moves, region

  # 1 グループの移動で空き領域を連結できる候補を、安い順に試す。
  active = [i for i, group in enumerate(groups[:-1]) if group.pos is not None]
  active.sort(key=lambda i: max(int(groups[i].v * R + 0.5), 1))
  best = None
  best_gain = -1
  for i in active[:32]:
    candidate = find_region(new_group.p, i)
    if candidate is None or not any(owner[x][y] == i for x, y in candidate):
      continue
    blocked = {x * N + y for x, y in candidate}
    destination = find_region(groups[i].p, i, blocked)
    if destination is None:
      continue
    income = int(new_group.v * compactness(candidate, new_group.p) + 0.5)
    cost = max(int(groups[i].v * R + 0.5), 1)
    if cost > income:
      continue
    gain = income - cost
    if gain > best_gain:
      best_gain = gain
      best = (i, destination, candidate)

  if best is None:
    return moves, None
  i, destination, region = best
  moves[i] = destination
  new_group.pos = region
  return moves, region

def move_groups(owner: List[List[int]], groups: List[GroupInfo], moves: List[List[Tuple[int, int]]], R: float) -> int:
  """
  グループを移動させる関数
  ### 入力
  - owner: 占有者のIDを保持するグリッド
  - groups: グループ情報のリスト
  - moves: 移動するグループの座標リスト [[(行, 列), ...], ...]
  - R: 移動コスト係数
  ### 出力
  - 移動コストの合計（int）
  """
  moved = [(i, pos) for i, pos in enumerate(moves) if pos]
  print(len(moved))

  # 同時移動なので、すべての旧領域を先に解放する。
  for i, _ in moved:
    for x, y in groups[i].pos:
      owner[x][y] = -1

  move_cost = 0
  for i, pos in moved:
    group = groups[i]
    for x, y in pos:
      owner[x][y] = i
    group.pos = pos
    new_c = compactness(pos, group.p)
    group.c = min(group.c, new_c)
    move_cost += max(int(group.v * R + 0.5), 1)

    print(i)
    for x, y in pos:
      print(x, y)

  return move_cost

def main():
  _n, _m, r = input().split()
  R = float(r)

  str_grid = [input() for _ in range(N)]
  # "#" -> 1, "." -> 0 に変換
  grid = [[1 if c == "#" else 0 for c in row] for row in str_grid]

  owner = [[-1] * N for _ in range(N)]  # 占有者のIDを保持するグリッド。-1は未占有を意味する。
  groups = []  # グループ情報のリスト
  money = 0  # 得られた金額

  for i in range(M):
    _gi, s, t, p, v = map(int, input().split())  # グループ情報の入力。_giはiと同じなので無視する。
    group = GroupInfo(s, t, p, v)
    groups.append(group)

    money += release_groups(groups, owner, s)  # 退去時刻が現在時刻 s より前のグループを解放する

    # 退去時刻が現在時刻 s より前のグループを解放し、料金を加算する
    money += release_groups(groups, owner, s)

    # 支払額が基準値を下回る場合は、配置せずにスキップする
    if v < expected_v(s, t, p) * K:
      print(0)
      print("No")
      continue

    # BFSで配置する。この際、移動も考慮する。
    moves, region = find_best_placement(grid, owner, groups, new_group=group, R=R)
    if region is not None:
      # すでに存在しているグループの移動
      move_cost = move_groups(owner, groups, moves, R)  # あとで実装する。
      # 移動コストを差し引く
      money -= move_cost
      # 今回新たに配置するグループの占有マスを更新
      print("Yes")
      for (x, y) in region:
        owner[x][y] = i
        print(x, y)
      # コンパクト度の更新
      group.c = compactness(region, p)
    else:
      print(0)
      print("No")

  ic(money)

if __name__ == "__main__":
  main()
