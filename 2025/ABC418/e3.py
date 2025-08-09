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

def d2e(dx, dy):
  gcd = math.gcd(dx, dy)  # 最大公約数
  # 最大公約数で割る
  ex = dx // gcd
  ey = dy // gcd
  # exが負ならば反転
  if ex < 0:
    ex = -ex
    ey = -ey
  # ex == 0 かつ ey < 0の場合も反転
  if ex == 0 and ey < 0:
    ex = -ex
    ey = -ey
  return (ex, ey)

def main():
  N = int(input())
  coord_list = [tuple(map(int, input().split())) for _ in range(N)]  # 点の座標

  edge_to_idx_dict = {}
  edge_count_list = []  # 辺の出現回数
  edge_list = [[] for _ in range(N*(N-1))]  # 辺iの両端の点の集合
  mid_to_idx_dict = {}
  mid_count_list = []  # 中点の出現回数

  for (x1, y1), (x2, y2) in itertools.combinations(coord_list, 2):
    dx = x2 - x1
    dy = y2 - y1
    
    ex, ey = d2e(dx, dy)  # 辺の大きさと方向を正規化

    if MyPC and (ex, ey) == (0, 1):
      ic(x1, y1, x2, y2)

    if (ex, ey) not in edge_to_idx_dict:
      edge_to_idx_dict[(ex, ey)] = len(edge_count_list)
      edge_count_list.append(1)
    else:
      edge_count_list[edge_to_idx_dict[(ex, ey)]] += 1

    ic(edge_to_idx_dict[(ex, ey)])
    edge_list[edge_to_idx_dict[(ex, ey)]].append(((x1, y1), (x2, y2)))

    mid = ((x1 + x2), (y1 + y2))  # 中点の座標を2倍したもの

    if mid not in mid_to_idx_dict:
      mid_to_idx_dict[mid] = len(mid_count_list)
      mid_count_list.append(1)
    else:
      mid_count_list[mid_to_idx_dict[mid]] += 1

  ic(edge_to_idx_dict)

  ic(edge_count_list)

  ans = 0

  for count in edge_count_list:
    ans += count * (count - 1) // 2

  # parallelogram_count = 0

  # 平行四辺形の除外
  for count in mid_count_list:
    ans -= count * (count - 1) // 2

  # ans -= parallelogram_count

  print(ans)

if __name__ == "__main__":
  main()