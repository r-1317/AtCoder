import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def step(grid, H, W):
  near_list = []
  to_white_list = []

  for i, row in enumerate(grid):
    for j, b in enumerate(row):
      if b:
        for dx in (-1, 0, 1):
          for dy in (-1, 0, 1):
            nx = i + dx
            ny = j + dy
            if 0 <= nx < H and 0 <= ny < W:
              near_list.append((nx, ny))
        to_white_list.append((i, j))

  new_grid = [row[:] for row in grid]

  while near_list:
    x, y = near_list.pop()
    new_grid[x][y] = True
  
  while to_white_list:
    x, y = to_white_list.pop()
    new_grid[x][y] = False

  return new_grid

def main():
  H, W = map(int, input().split())
  s_list = [(input()) for _ in range(H)]
  grid = [[True if c == "#" else False for c in s] for s in s_list]

  ic(grid)

  for _ in range(10):
    grid = step(grid, H, W)

    for row in grid:
      for b in row:
        print(int(b), end = " ")
      print()
    print("="*W*2)

if __name__ == "__main__":
  main()