import os
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def main():
  H, W = map(int, input().split())
  grid = [(input()) for _ in range(H)]
  N = int(input())
  r_c_e_list = [list(map(int, input().split())) for _ in range(N)]

  for i in range(N):
    r_c_e_list[i][0] -= 1
    r_c_e_list[i][1] -= 1

  medicine_dict = dict()
  for i, r_c_e in enumerate(r_c_e_list):
    r, c, e = r_c_e
    medicine_dict[(r, c)] = i

  adj_list = [[] for _ in range(N+1)]  # N番目はゴール
  for i, r_c_e in enumerate(r_c_e_list):
    r, c, e = r_c_e
    queue = [(r, c)]
    visited_list = [[False]*W for _ in range(H)]
    visited_list[r][c] = True
    for _ in range(e):
      new_queue = []
      for x, y in queue:
        for dx, dy in DIRS:
          nx, ny = x + dx, y + dy
          if not(0 <= nx < H and 0 <= ny < W) or grid[nx][ny] == "#":
            continue
          if not visited_list[nx][ny]:
            new_queue.append((nx, ny))
            visited_list[nx][ny] = True
            if (nx, ny) in medicine_dict:
              j = medicine_dict[(nx, ny)]
              adj_list[i].append(j)
            if grid[nx][ny] == "T":
              adj_list[i].append(N)
      queue = new_queue

  start_pos = (-1, -1)
  for i, row in enumerate(grid):
    for j, c in enumerate(row):
      if c == "S":
        start_pos = (i, j)

  if start_pos not in medicine_dict:
    print("No")
    sys.exit()
  start = medicine_dict[(start_pos)]
  visited_medicines = [False]*(N+1)
  visited_medicines[start] = True

  stack = [start]  # 実装が面倒なのでstackを採用
  while stack:
    u = stack.pop()
    for v in adj_list[u]:
      if not visited_medicines[v]:
        stack.append(v)
        visited_medicines[v] = True

  ic(visited_medicines)
  ic(adj_list)

  print("Yes" if visited_medicines[-1] else "No")

if __name__ == "__main__":
  main()