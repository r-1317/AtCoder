import os
from typing import Tuple, List
from collections import deque
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 20  # グリッドのサイズ。20固定

def is_valid_pos(x: int, y: int) -> bool:
  return 0 <= x < N and 0 <= y < N

def manhattan_dist(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
  """ マンハッタン距離を計算する """
  return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def nearest_valid(pos: Tuple[int, int], used: List[List[bool]]) -> Tuple[int, int]:
  """ 最寄りの未使用マスを探す """
  x, y = pos
  min_dist = float("inf")

  # BFSで最寄りの未使用マスを探索
  queue = deque()
  queue.append((x, y, 0))  # (x座標, y座標, 距離)
  visited = [[False] * N for _ in range(N)]
  visited[x][y] = True
  directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  while queue:
    cx, cy, dist = queue.popleft()

    if not used[cx][cy]:
      return (cx, cy)

    for dx, dy in directions:
      nx, ny = cx + dx, cy + dy
      if is_valid_pos(nx, ny) and not visited[nx][ny]:
        visited[nx][ny] = True
        queue.append((nx, ny, dist + 1))

  # 見つからなかった場合
  raise ValueError("No unused cell found")

def get_pair_pos(num: int, nums_idx_list: List[List[Tuple[int, int]]], other_pos: Tuple[int, int]) -> Tuple[int, int]:
  """
  numのもう一方の位置を返す
  入力:
    num: 対応する数字
    nums_idx_list: 各数字の位置を格納するリスト
    other_pos: 既に知っている位置
  出力:
    numのもう一方の位置
  """
  pos1, pos2 = nums_idx_list[num]
  return pos2 if pos1 == other_pos else pos1

def make_commands(collect_order: List[Tuple[int, int]], current_pos: Tuple[int, int]) -> List[str]:
  """
  収集順序に基づいてコマンド列を生成する
  入力:
    collect_order: 収集順序のリスト
    current_pos: 現在位置
  出力:
    コマンド列のリスト
  """

  commands = []
  x, y = current_pos

  for target in collect_order:
    tx, ty = target
    
    # 縦移動
    while x < tx:
      commands.append('D')
      x += 1
    while x > tx:
      commands.append('U')
      x -= 1
    # 横移動
    while y < ty:
      commands.append('R')
      y += 1
    while y > ty:
      commands.append('L')
      y -= 1
    commands.append('Z')  # 収集コマンド
    x, y = tx, ty

  return commands

def get_path_length(path: List[Tuple[int, int]]) -> int:
  """ 経路の長さを計算する """
  length = 0
  for i in range(1, len(path)):
    length += manhattan_dist(path[i-1], path[i])
  return length

def find_best_next_pos(collect_order: List[Tuple[int, int]], collect_stack: List[Tuple[int, int]], used: List[List[bool]], nums_idx_list: List[List[Tuple[int, int]]], grid: List[List[int]]) -> Tuple[int, int]:
  """
  次に収集するマスを決定する
  colect_ordrerの末尾と今回選択するマスの距離 + collect_stackの末尾と今回選択するマスの対のマスの距離 が最小になるマスを選ぶ
  入力:
    collect_order: 収集順序のリスト
    collect_stack: 2つめの数字を回収する際の経路のスタック
    used: 使用済みマスの管理リスト
    nums_idx_list: 各数字の位置を格納するリスト
    grid: グリッドの数字配置
  出力:
    次に収集するマスの位置
  """
  min_total_dist = float("inf")
  best_pos = None

  for i in range(N):
    for j in range(N):
      if used[i][j]:
        continue
      candidate_pos = (i, j)
      num = grid[i][j]
      pair_pos = get_pair_pos(num, nums_idx_list, candidate_pos)
      dist_1 = manhattan_dist(collect_order[-1], candidate_pos) if collect_order else 0  # collect_orderが空の場合は0
      dist_2 = manhattan_dist(collect_stack[-1], pair_pos) if collect_stack else 0  # collect_stackが空の場合は0
      total_dist = dist_1 + dist_2
      if total_dist < min_total_dist:
        min_total_dist = total_dist
        best_pos = candidate_pos

  return best_pos

def main():
  _ = int(input())  # Nは20で固定なので無視

  grid = [list(map(int, input().split())) for _ in range(N)]

  nums_idx_list = [[] for _ in range(N**2)]  # 各数字の位置を格納するリスト (各数字が2つずつ存在する)
  for i in range(N):
    for j in range(N):
      num = grid[i][j]
      nums_idx_list[num].append((i, j))
  
  used = [[False] * N for _ in range(N)]  # 使用済みマスの管理

  collect_order: List[Tuple[int, int]] = []  # 収集順序を格納するリスト

  current_pos = (0, 0)  # 現在位置

  collect_stack = []  # 2つめの数字を回収する際の経路のスタック


  for _ in range(N**2//2):
    # 最寄りの未使用マスを探す
    start = find_best_next_pos(collect_order, collect_stack, used, nums_idx_list, grid)  # 最寄りの未使用マスを探す
    num = grid[start[0]][start[1]]
    end = get_pair_pos(num, nums_idx_list, start)  # 対応するもう一方の位置を取得
    collect_order.append(start)  # 1つめの数字を回収
    collect_stack.append(end)  # 2つめの数字を後で回収するためにスタックに保存
    used[start[0]][start[1]] = True # 1つめの数字を使用済みにする
    used[end[0]][end[1]] = True  # 2つめの数字も便宜上使用済みにする
    current_pos = start  # 現在位置を更新

  # 回収スタックから2つめの数字を回収
  collect_order.extend(reversed(collect_stack))

  # 経路を出力
  commands = make_commands(collect_order, (0, 0))
  for cmd in commands:
    print(cmd)

if __name__ == "__main__":
  main()