import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def is_valid(x1, y1, x2, y2, grid):
  dx = x2 - x1
  dy = y2 - y1

  flag = True

  for i in range(dx+1):
    for j in range(dy+1):
      if grid[x1 + i][y1 + j] != grid[x2 - i][y2 - j]:
        flag = False

  return flag

def main():
  H, W = map(int, input().split())
  grid = [(input()) for _ in range(H)]

  ans = 0

  for x1 in range(H):
    for y1 in range(W):
      for x2 in range(x1, H):
        for y2 in range(y1, W):
          if is_valid(x1, y1, x2, y2, grid):
            ans += 1

  print(ans)

  # ic(is_valid(0, 0, 1, 0, grid))



if __name__ == "__main__":
  main()