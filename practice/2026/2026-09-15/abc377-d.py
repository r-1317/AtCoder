import os
from atcoder.segtree import SegTree

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

"""
使用例（区間和）
seg = SegmentTree(lambda a, b: a + b, lambda: 0, [1, 2, 3, 4])
seg.prod(1, 4)  # 9
seg.set(2, 10)
seg.all_prod()  # 17
"""

def op(a, b):
  return min(a, b)

def main():
  N, M = map(int, input().split())
  l_r_list = [list(map(int, input().split())) for _ in range(N)]
  l_r_list.sort(reverse=True)  # lが被った場合に最小値が入るように逆順

  seg = SegTree(op, M + 1, M + 1)
  for l, r in l_r_list:
    seg.set(l, r)

  ans = 0
  for i in range(1, M + 1):
    min_r = seg.prod(i, M + 1)
    ans += min_r - i

  ic(seg.get(1))
  print(ans)

if __name__ == "__main__":
  main()