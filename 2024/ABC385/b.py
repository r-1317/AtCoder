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
  h, w, x, y = map(int, input().split())
  grid = [["#"]*(w+2) for _ in range(h+2)]
  for i in range(1, h+1):
    grid[i] = ["#"] + list(input()) + ["#"]
  t_list = list(input())

  ans = 0
  adj_list = [(0, 1), (0, -1), (1, 0), (-1, 0)]

  for t in t_list:
    if t == "U" and grid[x-1][y] != "#":
      x -= 1
    elif t == "D" and grid[x+1][y] != "#":
      x += 1
    elif t == "L" and grid[x][y-1] != "#":
      y -= 1
    elif t == "R" and grid[x][y+1] != "#":
      y += 1
    if grid[x][y] == "@":
      ans += 1
      grid[x][y] = "."

  print(x, y, ans)


if __name__ == "__main__":
  main()