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
  grid = [input() for _ in range(H)]

  ans = True

  for i in range(H):
    for j in range(W):
      if grid[i][j] == '#':
        count = 0
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
          if 0 <= i + di < H and 0 <= j + dj < W and grid[i + di][j + dj] == '#':
            count += 1
        if not(count == 2 or count == 4):
          ans = False

  print("Yes" if ans else "No")

if __name__ == "__main__":
  main()