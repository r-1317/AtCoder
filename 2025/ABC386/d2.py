import sys


h, w = map(int, input().split())
s_list = [list(input()) for _ in range(h)]

grid = [["#"] * (w+2) for _ in range(h+2)]

for i in range(h):
  for j in range(w):
    grid[i+1][j+1] = s_list[i][j]

dp_list = [[[10**9] * (w+2) for _ in range(h+2)] for _ in range(2)]  # 0: 縦方向で来た, 1: 横方向で来た

for i in range(h+2):
  for j in range(w+2):
    if grid[i][j] == "S":
      start = (i, j)
    elif grid[i][j] == "G":
      goal = (i, j)

queue = [(start[0], start[1], 0), (start[0], start[1], 1)]

dp_list[0][start[0]][start[1]] = 0
dp_list[1][start[0]][start[1]] = 0

i = 0
ans = -1

while queue:
  i += 1
  prev_queue = queue
  queue = []
  while prev_queue:
    x, y, direction = prev_queue.pop(0)
    if direction == 0:  # 前の手が縦方向。つまり、今は横方向
      for dx in (-1, 1):
        if grid[x+dx][y] == "#":
          continue
        elif grid[x+dx][y] == "G":
          ans = i
          print(ans)
          sys.exit()
        elif i < dp_list[1][x+dx][y]:
          dp_list[1][x+dx][y] = i
          queue.append((x+dx, y, 1))
    else:  # 前の手が横方向。つまり、今は縦方向
      for dy in (-1, 1):
        if grid[x][y+dy] == "#":
          continue
        elif grid[x][y+dy] == "G":
          ans = i
          print(ans)
          sys.exit()
        elif i < dp_list[0][x][y+dy]:
          dp_list[0][x][y+dy] = i
          queue.append((x, y+dy, 0))

print(ans)