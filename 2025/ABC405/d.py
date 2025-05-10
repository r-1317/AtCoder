import os
from collections import deque

MyPC = os.path.basename(__file__) != "Main.py"
MyPC = False
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

D_LIST = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIR_LIST = ["v", "^", ">", "<"]

def main():
  h, w = map(int, input().split())
  s_list = [list(input()) for _ in range(h)]

  grid = [["#"]*(w+2) for _ in range(h+2)]

  for i in range(h):
    for j in range(w):
      grid[i+1][j+1] = s_list[i][j]
  # ic(grid)

  ic("------------")

  bfs_list = [[[10**9, ""] for _ in range(w+2)] for _ in range(h+2)]

  queue = deque()
  for i in range(h+2):
    for j in range(w+2):
      if grid[i][j] == "E":
        bfs_list[i][j] = [0, "E"]
        queue.append((i, j))
      elif grid[i][j] == "#":
        bfs_list[i][j] = [0, "#"]

  while queue:
    x, y = queue.popleft()
    for i in range(4):
      dx, dy = D_LIST[i]
      nx, ny = x + dx, y + dy
      if grid[nx][ny] == "#":
        continue
      if bfs_list[nx][ny][0] > bfs_list[x][y][0] + 1:
        bfs_list[nx][ny][0] = bfs_list[x][y][0] + 1
        bfs_list[nx][ny][1] = DIR_LIST[i]
        queue.append((nx, ny))
  
  for i in range(1, h+1):
    for j in range(1, w+1):
      print(bfs_list[i][j][1], end="")
    print()

if __name__ == "__main__":
  main()