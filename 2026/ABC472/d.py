import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def main():
  H, W, K = map(int, input().split())
  grid = [(input()) for _ in range(H)]
  dangerous_x_list = [False]*H
  dangerous_y_list = [False]*W

  for i in range(H):
    for j in range(W):
      c = grid[i][j]
      if c == "#":
        dangerous_x_list[i] = True
        dangerous_y_list[j] = True

  queue = []
  for i in range(H):
    for j in range(W):
      if not(dangerous_x_list[i] or dangerous_y_list[j]):
        queue.append((i, j))

  visited_list = [[False]*W for _ in range(H)]

  for x, y in queue:
    visited_list[x][y] = True

  for _ in range(K):
    new_queue = []
    for x, y in queue:
      for dx, dy in DIRS:
        nx = x + dx
        ny = y + dy
        if not(0 <= nx < H and 0 <= ny < W):
          continue
        if grid[nx][ny] == "#" or visited_list[nx][ny]:
          continue
        new_queue.append((nx, ny))
        visited_list[nx][ny] = True
    queue = new_queue

  ans = 0
  for i in range(H):
    for j in range(W):
      if visited_list[i][j]:
        ans += 1

  print(ans)


if __name__ == "__main__":
  main()