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

def get_neighbor_05(goal: Tuple[int, int]) -> List[Tuple[int, int]]:
  tx, ty = goal
  # directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
  cells = []
  for dx, dy in directions:
    for dist in range(1, 3):
      nx, ny = tx + dx * dist, ty + dy * dist
      cells.append((nx, ny))
  return cells

def get_neighbor_08(goal: Tuple[int, int]) -> List[Tuple[int, int]]:
  tx, ty = goal
  cells = []
  
  cells.append((tx, ty-1))
  cells.append((tx, ty+1))
  cells.append((tx-1, ty))
  cells.append((tx+2, ty))
  cells.append((tx+1, ty+1))
  cells.append((tx+1, ty-1))

  return cells

# (x, y)のマスの状態を返す
def cell_status(x: int, y: int, grid_BB: BitBoard) -> str:
  if not (0 <= x < grid_BB.N and 0 <= y < grid_BB.N):
    return "Not in grid"
  return "Tree" if grid_BB.is_set(x, y) else "Empty"

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

  # ランダムに並べ替え
  random.shuffle(empty_cells)

  default_add_list = []  # 木を追加する座標のリスト。出力の都合上、[x1, y1, x2, y2, ...]の1次元の形にする

  # 花を囲う
  # 花の下のマスが空きマスなら、入口が1つのみある形で囲う
  if cell_status(tx, ty+1, grid_BB) == "Empty":
    neighbor_cells = get_neighbor_08(goal)
  # 花の下のマスが木か盤面外なら、汎用の囲い方で囲う
  else:
    neighbor_cells = get_neighbor_05(goal)
  for cell in neighbor_cells:
    x, y = cell
    if is_valid(x, y, current_coord, goal, grid_BB, tentative_BB):
      grid_BB.set(x, y)
      empty_cells.remove((x, y))
      default_add_list.append(x)
      default_add_list.append(y)

  max_score = -1
  best_add_list = default_add_list[:]
  max_empty_cells = empty_cells[:]
  max_grid_BB = BitBoard(N, grid_BB.board)

  count = 0
  max_tree_num = N**2 // 4  # 木の最大数(N^2/4個まで)
  cell_swap_num = max_tree_num // 5  # 毎回入れ替える空きマスの数

  while True:
    count += 1
    ###### 後でやる ######

    add_list = default_add_list[:]  # 木を追加する座標のリスト。出力の都合上、[x1, y1, x2, y2, ...]の1次元の形にする
    tmp_grid_BB = BitBoard(N, grid_BB.board)  # grid_BBのコピー
    tmp_empty_cells = max_empty_cells[:]  # max_empty_cellsのコピー

    # 空きマスをランダムに入れ替える
    swap_idx_list_1 = random.sample(range(len(tmp_empty_cells)), cell_swap_num)
    swap_idx_list_2 = random.sample(range(len(tmp_empty_cells)), cell_swap_num)
    for i in range(cell_swap_num):
      idx1 = swap_idx_list_1[i]
      idx2 = swap_idx_list_2[i]
      tmp_empty_cells[idx1], tmp_empty_cells[idx2] = tmp_empty_cells[idx2], tmp_empty_cells[idx1]

    for i in range(max_tree_num):
      cell = tmp_empty_cells[i]
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
      max_empty_cells = tmp_empty_cells[:]
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