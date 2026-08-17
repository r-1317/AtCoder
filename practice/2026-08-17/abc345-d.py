import os
from itertools import permutations
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def find_start(grid):
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      if not grid[i][j]:
        return i, j

  return -1, -1

def search(N, H, W, a_b_list, p_list, grid, i):
  if i == N:
    x, y = find_start(grid)
    return x == -1

  x, y = find_start(grid)
  if x == -1:
    return True
  ans = False
  a, b = a_b_list[p_list[i]]
  if x + a <= H and y + b <= W:
    new_grid = [row[:] for row in grid]
    flag = True
    for j in range(x, x + a):
      for k in range(y, y + b):
        if new_grid[j][k]:
          flag = False
        new_grid[j][k] = True
    if flag:
      ans = ans or search(N, H, W, a_b_list, p_list, new_grid, i+1)
  if x + b <= H and y + a <= W:
    new_grid = [row[:] for row in grid]
    flag = True
    for j in range(x, x + b):
      for k in range(y, y + a):
        if new_grid[j][k]:
          flag = False
        new_grid[j][k] = True
    if flag:
      ans = ans or search(N, H, W, a_b_list, p_list, new_grid, i+1)

  return ans


def main():
  N, H, W = list(map(int, input().split()))  # Codonで動かすときに備えてlist
  a_b_list = [list(map(int, input().split())) for _ in range(N)]

  for p_list in permutations(list(range(N)), N):
    grid = [[False]*W for _ in range(H)]
    ans = search(N, H, W, a_b_list, p_list, grid, 0)
    if ans:
      print("Yes")
      sys.exit()

  print("No")

if __name__ == "__main__":
  main()