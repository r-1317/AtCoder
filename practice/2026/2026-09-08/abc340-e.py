import os
from atcoder.lazysegtree import LazySegTree

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def op(x, y):
  return max(x, y)

# def e():
#   return 0
e = 0

def mapping(f, x):
  return x + f

def composition(f,g):
  return f + g

# def id():
#   return 0
id = 0


def main():
  N, M = map(int, input().split())
  a_list = list(map(int, input().split()))
  b_list = list(map(int, input().split()))

  seg = LazySegTree(op, e, mapping, composition, id, a_list)

  for b in b_list:
    x = seg.get(b)
    seg.set(b, 0)

    all_count = x // N
    seg.apply(0, N, all_count)
    x -= all_count * N
    ic(x)
    
    r = min(N, b + 1 + x)
    seg.apply(b + 1, r, 1)
    x -= r - (b + 1)
    ic(x)
    
    seg.apply(0, x, 1)

  ans_list = []
  for i in range(N):
    ans_list.append(seg.get(i))

  print(*ans_list)


if __name__ == "__main__":
  main()