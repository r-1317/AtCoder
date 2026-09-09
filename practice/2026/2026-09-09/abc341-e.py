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
  return a + b

def e():
  return 0

def main():
  N, Q = map(int, input().split())
  S = input()

  a_list = []
  for i in range(N-1):
    a = 1 if S[i] != S[i+1] else 0
    a_list.append(a)

  seg = SegTree(lambda a, b: a + b, 0, a_list)

  for _ in range(Q):
    q, l, r = map(int, input().split())
    l -= 1
    r -= 1
    if q == 1:
      if l > 0:
        seg.set(l - 1, not(seg.get(l - 1)))
      if r < N - 1:
        seg.set(r, not(seg.get(r)))
    elif q == 2:
      ans = seg.prod(l, r) == r - l
      print("Yes" if ans else "No")

if __name__ == "__main__":
  main()