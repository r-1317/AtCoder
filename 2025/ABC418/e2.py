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

  ic(edge_to_idx_dict)

  ic(edge_count_list)

  ans = 0

  for count in edge_count_list:
    ans += count * (count - 1) // 2

  parallelogram_count = 0

  # 平行四辺形の除外
  multi_edge_list = []
  for i in range(len(edge_count_list)):
    if edge_count_list[i] > 1:
      for ((x1, y1), (x2, y2)), ((x3, y3), (x4, y4)) in itertools.combinations(edge_list[i], 2):
        # 平行四辺形の条件を満たすかチェック
        dx1 = x3 - x1
        dy1 = y3 - y1
        dx2 = x4 - x2
        dy2 = y4 - y2
        ex1, ey1 = d2e(dx1, dy1)
        ex2, ey2 = d2e(dx2, dy2)
        if ex1 == ex2 and ey1 == ey2:
          parallelogram_count += 1
        dx3 = x4 - x1
        dy3 = y4 - y1
        dx4 = x3 - x2
        dy4 = y3 - y2
        ex3, ey3 = d2e(dx3, dy3)
        ex4, ey4 = d2e(dx4, dy4)
        if ex3 == ex4 and ey3 == ey4:
          parallelogram_count += 1

  parallelogram_count //= 2  # 平行四辺形は2回カウントされているので半分にする

  ans -= parallelogram_count

  print(ans)

if __name__ == "__main__":
  main()