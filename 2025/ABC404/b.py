import os
import numpy as np

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  n = int(input())
  grid_s = [list(input()) for _ in range(n)]
  grid_t = [list(input()) for _ in range(n)]
  grid_s = np.array(grid_s)
  grid_t = np.array(grid_t)

  ans = 10**9

  for i in range(4):
    tmp_ans = i
    for j in range(n):
      for k in range(n):
        if grid_s[j][k] != grid_t[j][k]:
          tmp_ans += 1
    ans = min(ans, tmp_ans)
    grid_s = np.rot90(grid_s, -1)

  print(ans)

if __name__ == "__main__":
  main()