import os
import sys
from collections import deque

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def main():
  N = int(input())
  grid = [(input()) for _ in range(N)]

  p1 = None
  p2 = None

  for i in range(N):
    for j in range(N):
      if grid[i][j] == "P":
        if p1 is None:
          p1 = (i, j)
        else:
          p2 = (i, j)

  dist_list = [[[[10**9]*N for _ in range(N)] for _ in range(N)] for _ in range(N)]  # P1の(x, y), P2の(x, y)

  dist_list[p1[0]][p1[1]][p2[0]][p2[1]] = 0

  dq = deque()
  dq.append((p1[0], p1[1], p2[0], p2[1]))

  while dq:
    x1, y1, x2, y2 = dq.popleft()
    dist = dist_list[x1][y1][x2][y2]
    dist += 1  # この探索での距離

    for dx, dy in DIRS:
      nx1, ny1, nx2, ny2 = min(N - 1, max(0, x1 + dx)), min(N - 1, max(0, y1 + dy)), min(N - 1, max(0, x2 + dx)), min(N - 1, max(0, y2 + dy))
      if grid[nx1][ny1] == "#":
        nx1, ny1 = x1, y1
      if grid[nx2][ny2] == "#":
        nx2, ny2 = x2, y2
      if nx1 == nx2 and ny1 == ny2:
        print(dist)
        ic(nx1, ny1, nx2, ny2)
        sys.exit()
      if dist_list[nx1][ny1][nx2][ny2] > dist:
        dist_list[nx1][ny1][nx2][ny2] = dist
        dq.append((nx1, ny1, nx2, ny2))

  print(-1)

if __name__ == "__main__":
  main()