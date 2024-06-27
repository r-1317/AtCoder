import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def dist(i, n):
  if i%2 == 0:
    return range(n)
  else:
    return range(n-1, -1, -1)

def move(i, j):
  if i == 19 and j == 0:
    return None
  elif (i%2 == 0 and j == 19) or (i%2 == 1 and j == 0):
    print("D")
  elif i%2 == 0:
    print("R")
  else:
    print("L")

def main():
  n = int(input())
  grid = [list(map(int, input().split())) for _ in range(n)]

  ic(grid)

  soil = 0  # 今は使わない

  # 土を積む
  for i in range(n):
    for j in dist(i, n):
      ic(i, j)

      if 0 < grid[i][j]:
        print(f"+{grid[i][j]}")
      
      move(i,j)

  print("U\n"*19, end="")

  # 土を降ろす
  for i in range(n):
    for j in dist(i, n):
      ic(i, j)

      if grid[i][j] < 0:
        print(f"-{abs(grid[i][j])}")
      
      move(i,j)

if __name__ == "__main__":
  main()