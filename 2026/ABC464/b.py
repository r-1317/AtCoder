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

  grid = [list(input()) for _ in range(H)]

  for i in range(H):
    for j in range(W):
      grid[i][j] = True if grid[i][j] == "#" else False

  h = H
  w = W

  while not any(grid[0]):
    del grid[0]

  while not any(grid[-1]):
    del grid[-1]

  while True:
    flag = False
    for i in range(len(grid)):
      if grid[i][0]:
        flag = True
        break
    if flag:
      break
    for i in range(len(grid)):
      del grid[i][0]

  while True:
    flag = False
    for i in range(len(grid)):
      if grid[i][-1]:
        flag = True
        break
    if flag:
      break
    for i in range(len(grid)):
      del grid[i][-1]

  for row in grid:
    for b in row:
      print("#" if b else ".", end = "")
    print()

if __name__ == "__main__":
  main()