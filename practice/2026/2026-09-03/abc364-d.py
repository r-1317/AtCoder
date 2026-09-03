import os
import bisect

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def count(a_list, b, x):
  l_idx = bisect.bisect_left(a_list, b - x)
  r_idx = bisect.bisect_right(a_list, b + x)

  return r_idx - l_idx

def main():
  N, Q = map(int, input().split())
  a_list = list(map(int, input().split())) + [10**18, -10**18]
  a_list.sort()

  for _ in range(Q):
    b, k = map(int, input().split())
    # x = 2**31 - 1  # 0の場合にもたどり着けるようにする
    # stride = 2**30
    # while stride:
    #   if count(a_list, b, x) >= k:
    #     x -= stride
    #   else:
    #     x += stride
    #   stride //= 2
    l = -1
    r = 10**9
    while r - l > 1:
      mid = l + (r - l) // 2
      if count(a_list, b, mid) >= k:
        r = mid
      else:
        l = mid

    ic(r)
    print(r)


if __name__ == "__main__":
  main()