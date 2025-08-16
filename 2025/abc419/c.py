import os
import time

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

start_time = time.time()

def main():
  N = int(input())
  coord_list = [tuple(map(int, input().split())) for _ in range(N)]

  min_x = min(coord[0] for coord in coord_list)
  max_x = max(coord[0] for coord in coord_list)
  min_y = min(coord[1] for coord in coord_list)
  max_y = max(coord[1] for coord in coord_list)

  x_dist = (max_x - min_x)
  y_dist = (max_y - min_y)

  ans = (max(x_dist, y_dist) + 1) // 2

  print(ans)

if __name__ == "__main__":
  main()