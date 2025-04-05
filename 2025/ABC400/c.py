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

def main():
  n = int(input())
  # n = 10**18

  ans = 0

  for a in range(1, 100):  # 100は適当
    # 二分探索
    tmp_b = 10**18 // 2
    width = 10**18 // 4
    while width:
      x = 2**a * tmp_b**2
      if x < n:
        tmp_b += width
      else:
        tmp_b -= width
      width //= 2
    # 微調整
    for i in range(max(tmp_b - 100, 0), tmp_b + 100):
      x = 2**a * (i+1)**2
      if n < x:
        ans += i
        ic(a, i, x)
        break
      # ic(a, i+1, x)
    # ic(a, tmp_b, i)
    if 2 <= i:
      ans -= 1

  print(ans)


if __name__ == "__main__":
  main()