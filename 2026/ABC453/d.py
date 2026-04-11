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

index_dict = {"U": 0, "D": 1, "L": 2, "R": 3}
udlr = ["U", "D", "L", "R"]
d_to_index = {(-1, 0): 0, (1, 0): 1, (0, -1): 2, (0, 1): 3}
index_to_dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]

rev_d_to_index = {(1, 0): 0, (-1, 0): 1, (0, 1): 2, (0, -1): 3}
rev_index_to_dir = [(1, 0),(-1, 0), (0, 1), (0, -1)]

def main():
  H, W = map(int, input().split())

  s_list = [list(input()) for _ in range(H)]

  grid = [["#"]*(W+2) for _ in range(H+2)]

  start = (-1, -1)
  goal = (-1, -1)

  for i in range(H):
    for j in range(W):
      grid[i+1][j+1] = s_list[i][j]
      if s_list[i][j] == "S":
        start = (i+1, j+1)
      elif s_list[i][j] == "G":
        goal = (i+1, j+1)

  ic(grid)

  bfs_list = [[[False]*4 for _ in range(W+2)] for _ in range(H+2)]

  queue = [(start[0], start[1], 1)]
  while queue:
    x, y, prev_dir = queue.pop()
    if grid[x][y] == "G":
      break
    if grid[x][y] == "#":
      continue

    if grid[x][y] == "o":
      dx, dy = index_to_dir[prev_dir]
      nx, ny = x + dx, y + dy
      new_dir = prev_dir
      if bfs_list[nx][ny][new_dir]:
        continue
      bfs_list[nx][ny][new_dir] = True
      queue.append((nx, ny, new_dir))
    
    if grid[x][y] == "x":
      x_flag = True
    else:
      x_flag = False

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
      nx, ny = x + dx, y + dy
      new_dir = d_to_index[(dx, dy)]
      # ic(new_dir)

      if x_flag and new_dir == prev_dir:
        continue
      if bfs_list[nx][ny][new_dir]:
        continue

      bfs_list[nx][ny][new_dir] = True
      queue.append((nx, ny, new_dir))

  if not any(bfs_list[goal[0]][goal[1]]):
    print("No")
    sys.exit()

  ans = ""

  visited_list = [[[False] for _ in range(W+2)] for _ in range(H+2)]
  x, y = goal
  prev_dir = -1
  for i in range(4):
    if bfs_list[x][y][i]:
      prev_dir = i
      break
  visited_list[x][y] = True

  while True:
    if grid[x][y] == "S":
      break
    if grid[x][y] == "o":
      o_flag = True
    else:
      o_flag = False
    if grid[x][y] == "x":
      x_flag = True
    else:
      x_flag = False
    for i in range(4):
      if not bfs_list[x][y][i]:
        continue
      if o_flag and i != prev_dir:
        continue
      if x_flag and i == prev_dir:
        continue
      rx, ry = rev_index_to_dir[i]
      nx, ny = rx + x, ry + y
      prev_dir = i
      x, y = nx, ny
      ans += udlr[i]

  print("Yes")
  print(ans)

if __name__ == "__main__":
  main()