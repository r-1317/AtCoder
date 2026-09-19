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

def main():
  N, M = map(int, input().split())
  p_list = list(map(int, input().split()))

  idx_list = [-1]*(N+1)
  for i, p in enumerate(p_list):
    idx_list[p] = i

  min_seg = SegTree(lambda a, b: min(a, b), 10**9, p_list[:])
  max_seg = SegTree(lambda a, b: max(a, b), -1, p_list[:])

  for _ in range(M):
    l, r = map(int, input().split())
    l -= 1
    r -= 1
    current_min = min_seg.prod(l, r + 1)
    current_max = max_seg.prod(l, r + 1)
    min_idx = idx_list[current_min]
    max_idx = idx_list[current_max]

    # 逆にする(処理に注意)
    min_seg.set(min_idx, current_max)
    min_seg.set(max_idx, current_min)
    max_seg.set(min_idx, current_max)
    max_seg.set(max_idx, current_min)
    idx_list[current_min] = max_idx
    idx_list[current_max] = min_idx

  ans_list = [min_seg.get(i) for i in range(N)]

  print(*ans_list)

if __name__ == "__main__":
  main()