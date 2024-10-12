import os
from math import sqrt

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
  coord_list = [list(map(int, input().split())) for _ in range(n)] + [[0, 0]]

  tmp_coord = [0, 0]

  cost = 0

  for i in range(n+1):
    x, y = coord_list[i]
    tmp_x, tmp_y = tmp_coord

    ic(x, y, tmp_x, tmp_y)

    cost += sqrt((x - tmp_x)**2 + (y - tmp_y)**2)

    tmp_coord = coord_list[i]

  print(cost)

if __name__ == "__main__":
  main()