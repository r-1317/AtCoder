import os
import math

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
    n = int(input())

    a = math.isqrt(n)  # √N 以下の最大の平方根のはず
    ans = 2*a*(a-1)

    # 残りを敷き詰める
    rest = n - a**2  # 残りの枚数。restであっているのかは知らん
    if rest > 0:
      ans += rest*2
      ans -= 1
      if rest > a:  # 角まではみ出る場合
        ans -= 1
    
    ic(ans)
    print(ans)


if __name__ == "__main__":
  main()