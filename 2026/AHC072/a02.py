import os
import sys
from collections import deque
from typing import Tuple, List

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def read_input() -> Tuple[int, int, List[List[List[int]]], List[Tuple[int, int]], List[List[bool]]]:
  N, K = map(int, input().split())
  towers: List[List[List[int]]] = [[[] for _ in range(N)] for _ in range(N)]
  nests: List[Tuple[int, int]] = [(-1, -1) for _ in range(K)]
  walls: List[List[bool]] = [[False] * N for _ in range(N)]

  for i in range(N):
    for j, cell in enumerate(input().strip()):
      if cell == "#":
        walls[i][j] = True
      elif "a" <= cell <= "l":
        towers[i][j].append(ord(cell) - ord("a"))
      elif "A" <= cell <= "L":
        nests[ord(cell) - ord("A")] = (i, j)

  return N, K, towers, nests, walls

def get_shortest_path(N: int, walls: List[List[bool]], towers: List[List[List[int]]], start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int, int, str, int]]:
  directions = ((-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R"))
  previous = {start: None}
  queue = deque([start])

  while queue and goal not in previous:
    i, j = queue.popleft()
    k = len(towers[i][j]) - (1 if (i, j) == start else 0)
    for di, dj, d in directions:
      for distance in range(1, k + 2):
        ni, nj = i + di * distance, j + dj * distance
        if not (0 <= ni < N and 0 <= nj < N) or walls[ni][nj]:
          break
        if len(towers[ni][nj]) >= 8 or (ni, nj) in previous:
          continue
        previous[(ni, nj)] = ((i, j), d, distance)
        queue.append((ni, nj))

  if goal not in previous:
    raise ValueError("No path to the goal")

  path = []
  pos = goal
  while pos != start:
    prev, d, distance = previous[pos]
    # 通過するマスでは、移動中の1匹が元の塔の上に乗っている。
    k = len(towers[prev[0]][prev[1]]) - (1 if prev == start else 0)
    path.append((prev[0], prev[1], k, d, distance))
    pos = prev
  path.reverse()
  return path

def move_tower(towers: List[List[List[int]]], nests: List[Tuple[int, int]], step: Tuple[int, int, int, str, int]) -> List[List[List[int]]]:
  i, j, k, d, distance = step
  di, dj = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}[d]
  ni, nj = i + di * distance, j + dj * distance

  moving = towers[i][j][k:]
  del towers[i][j][k:]
  towers[ni][nj].extend(reversed(moving))

  for row, col in ((i, j), (ni, nj)):
    for color, nest in enumerate(nests):
      if nest == (row, col):
        while towers[row][col] and towers[row][col][-1] == color:
          towers[row][col].pop()
        break

  return towers

def main():
  N, K, towers, nests, walls = read_input()

  ans_list: List[Tuple[int, int, int, str, int]] = []

  # 1匹ずつ巣に帰す
  for i in range(N):
    for j in range(N):
      if towers[i][j]:
        color = towers[i][j][0]
        path = get_shortest_path(N, walls, towers, (i, j), nests[color])
        for step in path:
          ans_list.append(step)
          towers = move_tower(towers, nests, step)

  for step in ans_list:
    print(*step)

  print(f"score: {len(ans_list)}", file=sys.stderr)  # スコアを標準エラー出力に表示 (すべてのスライムが帰巣できている前提でのスコア計算)

if __name__ == "__main__":
  main()
