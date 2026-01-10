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

# def get_path(start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
#   """ startからendまでの経路を返す（単純なL字型の経路） """
#   path = []
#   x1, y1 = start
#   x2, y2 = end

#   # 横に移動
#   step = 1 if x2 >= x1 else -1
#   for x in range(x1, x2, step):
#     path.append((x, y1))
  
#   # 縦に移動
#   step = 1 if y2 >= y1 else -1
#   for y in range(y1, y2 + step, step):
#     path.append((x2, y))
  
#   return path

def nearest_unused(pos: Tuple[int, int], used: List[List[bool]]) -> Tuple[int, int]:  # 最寄りの未使用マスを探す
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

  for _ in range(N**2//2):
    # 最寄りの未使用マスを探す
    start = nearest_unused(current_pos, used)
    num = grid[start[0]][start[1]]
    end = get_pair_pos(num, nums_idx_list, start)  # 対応するもう一方の位置を取得
    collect_order.append(start)
    collect_order.append(end)
    # ２つのマスを使用済みにする
    used[start[0]][start[1]] = True
    used[end[0]][end[1]] = True
    current_pos = end  # 現在位置を更新

  # 経路を出力
  commands = make_commands(collect_order, (0, 0))
  for cmd in commands:
    print(cmd)

if __name__ == "__main__":
  main()