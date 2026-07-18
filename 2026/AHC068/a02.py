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

def main():
  grid, v_walls, h_walls = read_input()

  ans_list = []  # 入れ替え操作のリスト

  size = N * N
  neighbors = [[] for _ in range(size)]
  for r in range(N):
    for c in range(N):
      u = r * N + c
      if c + 1 < N and not v_walls[r][c]:
        neighbors[u].append(u + 1)
        neighbors[u + 1].append(u)
      if r + 1 < N and not h_walls[r][c]:
        neighbors[u].append(u + N)
        neighbors[u + N].append(u)

  parent = [-1] * size
  parent[0] = 0
  order = [0]
  for u in order:
    for v in neighbors[u]:
      if parent[v] == -1:
        parent[v] = u
        order.append(v)

  pos = [0] * size
  for r in range(N):
    for c in range(N):
      pos[grid[r][c]] = r * N + c

  active = [True] * size
  for target in reversed(order[1:]):
    source = pos[target]
    if source != target:
      prev = [-1] * size
      prev[source] = source
      queue = deque([source])
      while prev[target] == -1:
        u = queue.popleft()
        for v in neighbors[u]:
          if active[v] and prev[v] == -1:
            prev[v] = u
            queue.append(v)

      path = []
      u = target
      while u != source:
        path.append(u)
        u = prev[u]
      path.reverse()

      u = source
      for v in path:
        ur, uc = divmod(u, N)
        vr, vc = divmod(v, N)
        card_u = grid[ur][uc]
        card_v = grid[vr][vc]
        grid[ur][uc], grid[vr][vc] = card_v, card_u
        pos[card_u] = v
        pos[card_v] = u
        if ur == vr:
          ans_list.append(('H', ur, min(uc, vc), 1, 2))
        else:
          ans_list.append(('V', min(ur, vr), uc, 2, 1))
        u = v

    active[target] = False

  for d, r, c, h, w in ans_list:
    print(d, r, c, h, w)


if __name__ == "__main__":
  main()
