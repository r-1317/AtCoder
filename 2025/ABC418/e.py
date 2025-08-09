import os
import math
import itertools

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  N = int(input())
  coord_list = [tuple(map(int, input().split())) for _ in range(N)]  # 点の座標

  edge_to_idx_dict = {}
  edge_count_list = []  # 辺の出現回数

  for (x1, y1), (x2, y2) in itertools.combinations(coord_list, 2):
    dx = x2 - x1
    dy = y2 - y1
    gcd = math.gcd(dx, dy)  # 最大公約数
    # 最大公約数で割る
    ex = dx // gcd
    ey = dy // gcd
    # exが負ならば反転
    if ex < 0:
      ex = -ex
      ey = -ey

    if MyPC and (ex, ey) == (0, 1):
      ic(x1, y1, x2, y2)

    if (ex, ey) not in edge_to_idx_dict:
      edge_to_idx_dict[(ex, ey)] = len(edge_count_list)
      edge_count_list.append(1)
    else:
      edge_count_list[edge_to_idx_dict[(ex, ey)]] += 1

  ic(edge_to_idx_dict)

  ic(edge_count_list)

  ans = 0

  for count in edge_count_list:
    ans += count * (count - 1) // 2

  print(ans)

if __name__ == "__main__":
  main()