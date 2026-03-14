import os
from typing import Tuple, List

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 200

def main():
  _ = int(input())  # Nは200で固定されているため、入力は無視する
  grid = [list(map(int, input().split())) for _ in range(N)]

  routes = []
  for i in range(N):
    tmp_route = [(i, j) for j in range(N)]
    if i % 2 == 1:
      tmp_route.reverse()
    routes.extend(tmp_route)

  for route in routes:
    print(*route)

if __name__ == "__main__":
  main()