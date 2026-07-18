import os
from collections import deque
from typing import Tuple, List
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 20  # 固定

def read_input() -> Tuple[List[List[int]], List[List[bool]], List[List[bool]]]:
  """
  入力を読み込む関数
  入力:
    - なし
  出力:
    - grid: 各マスのカードの番号を格納した2次元リスト
    - v_walls: 縦の壁の情報を格納した2次元リスト
    - h_walls: 横の壁の情報を格納した2次元リスト
  """
  _ = int(input())  # Nの入力は無視
  grid = [list(map(int, input().split())) for _ in range(N)]  # 各マスのカードの番号

  v_walls = [[False]*N for _ in range(N)]  # 縦の壁の情報
  for i in range(N):
    wall_str = input()
    for j in range(N-1):
      if wall_str[j] == '1':
        v_walls[i][j] = True
  h_walls = [[False]*N for _ in range(N)]  # 横の壁の情報
  for i in range(N-1):
    wall_str = input()
    for j in range(N):
      if wall_str[j] == '1':
        h_walls[i][j] = True

  return grid, v_walls, h_walls

def swap_cards(grid: List[List[int]], v_walls: List[List[bool]], h_walls: List[List[bool]], d: int, r: int, c: int, h: int, w: int) -> bool:
  """
  カードを入れ替える関数
  入力:
    - grid: 各マスのカードの番号を格納した2次元リスト
    - v_walls: 縦の壁の情報を格納した2次元リスト
    - h_walls: 横の壁の情報を格納した2次元リスト
    - d: 入れ替え方向 (0: 縦, 1: 横)
    - r: 入れ替え対象の左上の行番号
    - c: 入れ替え対象の左上の列番号
    - h: 入れ替え対象の高さ
    - w: 入れ替え対象の幅
  出力:
    - 入れ替えが成功したかどうか (bool)
  """
  if d != 0 and d != 1:
    return False
  if r < 0 or c < 0 or h <= 0 or w <= 0 or r + h > N or c + w > N:
    return False
  if (h if d == 0 else w) & 1:
    return False

  for i in range(r, r + h):
    walls = v_walls[i]
    for j in range(c, c + w - 1):
      if walls[j]:
        return False

  for i in range(r, r + h - 1):
    walls = h_walls[i]
    for j in range(c, c + w):
      if walls[j]:
        return False

  if d == 0:
    half = h // 2
    for i in range(r, r + half):
      other = i + half
      grid[i][c:c+w], grid[other][c:c+w] = grid[other][c:c+w], grid[i][c:c+w]
  else:
    half = w // 2
    right = c + half
    for i in range(r, r + h):
      row = grid[i]
      row[c:right], row[right:c+w] = row[right:c+w], row[c:right]

  return True


# 評価関数
def evaluate_01(grid: List[List[int]], v_walls: List[List[bool]], h_walls: List[List[bool]]) -> float:
  """
  評価関数
  各カードごとの目的の位置までの最短経路の長さのp乗の総和を計算する
  入力:
    - grid: 各マスのカードの番号を格納した2次元リスト
    - v_walls: 縦の壁の情報を格納した2次元リスト
    - h_walls: 横の壁の情報を格納した2次元リスト
  出力:
    - 評価値 (float)
  """

  p = 1.0  # p乗の指数

  cache = getattr(evaluate_01, "_distance_cache", None)
  if cache is None or cache[0] is not v_walls or cache[1] is not h_walls:
    size = N * N
    neighbors = [[] for _ in range(size)]
    for r in range(N):
      base = r * N
      for c in range(N):
        u = base + c
        if c + 1 < N and not v_walls[r][c]:
          neighbors[u].append(u + 1)
          neighbors[u + 1].append(u)
        if r + 1 < N and not h_walls[r][c]:
          neighbors[u].append(u + N)
          neighbors[u + N].append(u)

    distances = []
    for start in range(size):
      dist = [-1] * size
      dist[start] = 0
      queue = deque([start])
      while queue:
        u = queue.popleft()
        next_dist = dist[u] + 1
        for v in neighbors[u]:
          if dist[v] == -1:
            dist[v] = next_dist
            queue.append(v)
      distances.append(dist)
    evaluate_01._distance_cache = (v_walls, h_walls, distances)
  else:
    distances = cache[2]

  total = 0.0
  for r, row in enumerate(grid):
    position = r * N
    for c, card in enumerate(row):
      distance = distances[position + c][card]
      total += distance ** p
  return total

def greedy_swap(grid: List[List[int]], v_walls: List[List[bool]], h_walls: List[List[bool]]) -> Tuple[int, int, int, int, int]:
  """
  貪欲法で入れ替え操作を行う関数
  入力:
    - grid: 各マスのカードの番号を格納した2次元リスト
    - v_walls: 縦の壁の情報を格納した2次元リスト
    - h_walls: 横の壁の情報を格納した2次元リスト
  出力:
    - 入れ替え操作 (Tuple[int, int, int, int, int])
      各値は (d, r, c, h, w) の形式で、入れ替え方向、左上の行番号、左上の列番号、高さ、幅を表す
  """
  while True:
    best_eval = evaluate_01(grid, v_walls, h_walls)
    best_swap = None

    for d in range(2):
      for r in range(N):
        for c in range(N):
          for h in range(1, 4):
            for w in range(1, 4):
              if swap_cards(grid, v_walls, h_walls, d, r, c, h, w):
                current_eval = evaluate_01(grid, v_walls, h_walls)
                if current_eval < best_eval:
                  best_eval = current_eval
                  best_swap = (d, r, c, h, w)
                swap_cards(grid, v_walls, h_walls, d, r, c, h, w)  # 元に戻す

    if best_swap is None:
      break

    d, r, c, h, w = best_swap
    swap_cards(grid, v_walls, h_walls, d, r, c, h, w)

  return best_swap

def count_vailable_swaps(grid: List[List[int]], v_walls: List[List[bool]], h_walls: List[List[bool]]) -> int:
  """
  入れ替え可能な操作の数を数える関数(検証用の関数)
  入力:
    - grid: 各マスのカードの番号を格納した2次元リスト
    - v_walls: 縦の壁の情報を格納した2次元リスト
    - h_walls: 横の壁の情報を格納した2次元リスト
  出力:
    - 入れ替え可能な操作の数 (int)
  """
  count = 0
  for d in range(2):
    for r in range(N):
      for c in range(N):
        for h in range(1, 21):
          for w in range(1, 21):
            if swap_cards(grid, v_walls, h_walls, d, r, c, h, w):
              count += 1

  return count

def main():
  grid, v_walls, h_walls = read_input()

  ans_list = []  # 入れ替え操作のリスト

  print(count_vailable_swaps(grid, v_walls, h_walls))  # 入れ替え可能な操作の数を出力

  # sys.exit()

  # 貪欲法
  for _ in range(10**1):  # 最大10**5回の入れ替え操作を行う
    swap = greedy_swap(grid, v_walls, h_walls)
    ic(swap)
    if swap is None:
      break
    ans_list.append(swap)
    if evaluate_01(grid, v_walls, h_walls) < 0.9:  # すべてのカードが目的の位置に到達したら終了
      break

  ic(len(ans_list))

  for d, r, c, h, w in ans_list:
    print(d, r, c, h, w)


if __name__ == "__main__":
  main()
