import os
import math
from atcoder.segtree import SegTree
import bisect

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None



def main():
  T = int(input())

  for _ in range(T):
    N = int(input())
    degree_list = []  # 角度の配列
    for _ in range(N):
      x, y = map(int, input().split())
      degree_list.append(math.degrees(math.atan2(y, x)))

    degree_list.sort()
    ic(degree_list)
    degree_list.extend(degree_list[:])  # 

    ans = 0
    for i in range(N):
      l_degree = degree_list[i]
      r_degree = l_degree + 180.0
      if r_degree >= 180.0:  # 途中で0度のところを超える場合
        r_degree = r_degree - 360.0
        r_idx = bisect.bisect(degree_list, r_degree)
        if r_idx == 0 and degree_list[r_idx] > r_degree:  # 満たない場合
          r_idx = -1
        current_ans = (N - 1 - i) + (r_idx + 1)
      else:
        r_idx = bisect.bisect(degree_list, r_degree)
        current_ans = r_idx - i
      current_ans = max(current_ans, N - current_ans)
      ans = max(ans, current_ans)

    print(ans)

if __name__ == "__main__":
  main()