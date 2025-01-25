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
  h, w = map(int, input().split())
  grid = [list(input()) for _ in range(h)]
  x_min, y_min, x_max, y_max = 10**9, 10**9, -(10**9), -(10**9)

  for i in range(h):
    for j in range(w):
      if grid[i][j] == "#":
        x_min = i if i < x_min else x_min
        y_min = j if j < y_min else y_min
        x_max = i if i > x_max else x_max
        y_max = j if j > y_max else y_max
  
  flag = True

  for i in range(x_min, x_max+1):
    for j in range(y_min, y_max+1):
      if grid[i][j] == ".":
        flag = False
        break

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()