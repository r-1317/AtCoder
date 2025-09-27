import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  H, W = map(int, input().split())
  str_grid = [input() for _ in range(H)]

  grid = [[0] * W for _ in range(H)]
  for i in range(H):
    for j in range(W):
      if str_grid[i][j] == "#":
        grid[i][j] = 1

  queue = []

  # キューの初期化
  for i in range(H):
    for j in range(W):
      if grid[i][j] == 1:
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
          ni = i + di
          nj = j + dj
          queue.append((ni, nj))
  
  while queue:
    next_queue = []
    fill_positions = []
    for i, j in queue:
      if not (0 <= i < H and 0 <= j < W):
        continue
      neighbor_count = 0
      for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni = i + di
        nj = j + dj
        if 0 <= ni < H and 0 <= nj < W and grid[ni][nj] == 1:
          neighbor_count += 1
      if neighbor_count == 1 and grid[i][j] == 0:
        fill_positions.append((i, j))
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
          ni = i + di
          nj = j + dj
          next_queue.append((ni, nj))
    queue = next_queue
    for i, j in fill_positions:
      grid[i][j] = 1

  ans = sum([sum(row) for row in grid])
  print(ans)

  ic(grid)

if __name__ == "__main__":
  main()