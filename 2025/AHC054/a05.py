import os
from typing import List, Tuple
import random
import time
from collections import deque
import sys

MyPC = os.path.basename(__file__) != "Main.py"
MyPC = False
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

random.seed(1317)

start_time = time.time()
TIME_LIMIT = 1.8  # 秒
TIME_LIMIT = 50  # テスト用

# NxNの盤面をビットボードで表現する
class BitBoard:
  # N: 盤面のサイズ, board: ビットボードの初期値(指定しない場合はすべて0)
  def __init__(self, N: int, board: int = 0):
    self.N = N
    self.board = board

  # (x, y)のマスを1にする
  def set(self, x: int, y: int):
    self.board |= (1 << (x * self.N + y))

  # (x, y)のマスを0にする
  def unset(self, x: int, y: int):
    self.board &= ~(1 << (x * self.N + y))

  # (x, y)のマスが1かどうかを返す
  def is_set(self, x: int, y: int) -> bool:
    return (self.board >> (x * self.N + y)) & 1 == 1

  # ビットボードを文字列で表示する
  def __str__(self):
    res = []
    for i in range(self.N):
      row = []
      for j in range(self.N):
        if self.is_set(i, j):
          row.append('1')
        else:
          row.append('0')
      res.append(''.join(row))
    return '\n'.join(res)

# マスの評価値を計算する関数(a02.pyで使用)
def eval02(x: int, y: int, goal: Tuple[int, int], start: Tuple[int, int]) -> float:
  # goal: (tx, ty), start: (sx, sy)
  tx, ty = goal
  sx, sy = start
  return abs(x - tx) + abs(y - ty) + 1e-4 * (abs(x - sx) + abs(y - sy))

# (x, y)に木を追加してもよいかどうかを判定する関数
def is_valid(x: int, y: int, current_coord: Tuple[int, int], goal: Tuple[int, int], grid_BB: BitBoard, tentative_BB: BitBoard) -> bool:
  # まず、(x, y)が盤面の範囲内かどうかを判定
  if x < 0 or x >= grid_BB.N or y < 0 or y >= grid_BB.N:
    return False
  # 次に、(x, y)がすでに木があるマスかどうかを判定
  if grid_BB.is_set(x, y):
    return False
  # 次に、(x, y)がゴールマスかどうかを判定
  if (x, y) == goal:
    return False
  # 次に、(x, y)が確認済みマスかどうかを判定
  if tentative_BB.is_set(x, y):
    return False
  # 最後に、(x, y)に木をおいても現在地からゴールまでの経路が存在するかどうかを判定
  queue = [current_coord]
  visited = BitBoard(grid_BB.N)
  visited.set(current_coord[0], current_coord[1])
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  while queue:
    cx, cy = queue.pop(0)
    if (cx, cy) == goal:
      return True
    for dx, dy in directions:
      nx, ny = cx + dx, cy + dy
      if 0 <= nx < grid_BB.N and 0 <= ny < grid_BB.N:
        if not grid_BB.is_set(nx, ny) and not visited.is_set(nx, ny) and not (nx == x and ny == y):
          visited.set(nx, ny)
          queue.append((nx, ny))
  return False

def shortest_path_length(start: Tuple[int, int], goal: Tuple[int, int], grid_BB: BitBoard) -> int:
  if start == goal:
    return 0
  queue = deque([start])
  visited = BitBoard(grid_BB.N)
  visited.set(start[0], start[1])
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  distance = 0
  while queue:
    distance += 1
    for _ in range(len(queue)):
      cx, cy = queue.popleft()
      for dx, dy in directions:
        nx, ny = cx + dx, cy + dy
        if 0 <= nx < grid_BB.N and 0 <= ny < grid_BB.N:
          if not grid_BB.is_set(nx, ny) and not visited.is_set(nx, ny):
            if (nx, ny) == goal:
              return distance
            visited.set(nx, ny)
            queue.append((nx, ny))
  return 10**9  # ゴールに到達できない場合


def main():
  N, tx, ty = map(int, input().split())
  goal = (tx, ty)
  grid = [input() for _ in range(N)]

  current_coord = (0, N//2)  # 直前の座標

  grid_BB = BitBoard(N)
  for i in range(N):
    for j in range(N):
      if grid[i][j] == "T":
        grid_BB.set(i, j)

  tentative_BB = BitBoard(N)  # 確認済みマスを1にするビットボード
  tentative_BB.set(current_coord[0], current_coord[1])

  # すべての空きマスを配列に格納
  empty_cells = []
  for i in range(N):
    for j in range(N):
      if not grid_BB.is_set(i, j):
        empty_cells.append((i, j))

  max_score = -1
  best_add_list = []
  max_grid_BB = BitBoard(N, grid_BB.board)

  count = 0

  while True:
    count += 1
    # ランダムに並べ替え
    random.shuffle(empty_cells)

    add_list = []  # 木を追加する座標のリスト。出力の都合上、[x1, y1, x2, y2, ...]の1次元の形にする
    tmp_grid_BB = BitBoard(N, grid_BB.board)  # grid_BBのコピー

    for i in range(100):  # 木の最大数を100に制限
      cell = empty_cells[i]
      x, y = cell
      if is_valid(x, y, current_coord, goal, tmp_grid_BB, tentative_BB):
        add_list.append(x)
        add_list.append(y)
        tmp_grid_BB.set(x, y)

    # 最短経路の長さを計算
    initial_path_length = shortest_path_length(current_coord, goal, tmp_grid_BB)
    # print(f"Score: {initial_path_length}", file=sys.stderr)

    if max_score < initial_path_length:
      max_score = initial_path_length
      best_add_list = add_list
      max_grid_BB = BitBoard(N, tmp_grid_BB.board)
      print(f"New best score: {max_score}", file=sys.stderr)

    # 制限時間を超えたら終了
    if TIME_LIMIT < time.time() - start_time:
      break

  add_list = best_add_list
  grid_BB = max_grid_BB

  print(f"試行回数: {count}", file=sys.stderr)

  # 最初のターン
  next_coord = tuple(map(int, input().split()))  # 次に移動する座標
  revealed_cells = list(map(int, input().split()))  # 確認済みマスのリスト
  for i in range(1, len(revealed_cells), 2):
    x, y = revealed_cells[i], revealed_cells[i+1]
    tentative_BB.set(x, y)
  # (制約上、最初のターンでゴールに到達することはない)
  # 配置する木を出力
  print(len(add_list) // 2, end=' ')
  print(*add_list)
  current_coord = next_coord

  while True:
    next_coord = tuple(map(int, input().split()))  # 次に移動する座標
    revealed_cells = list(map(int, input().split()))  # 確認済みマスのリスト
    # revealed_cellsの最初の要素は確認済みマスの数
    # 以降の要素は(x1, y1, x2, y2, ..., xk, yk)の形式で与えられる
    for i in range(1, len(revealed_cells), 2):
      x, y = revealed_cells[i], revealed_cells[i+1]
      tentative_BB.set(x, y)
    # 次に移動する座標がゴールなら終了
    if next_coord == goal:
      break
    print(0)
    current_coord = next_coord

if __name__ == "__main__":
  main()