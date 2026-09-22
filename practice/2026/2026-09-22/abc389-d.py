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
  R = int(input())

  ans = 0
  for i in range(R):
    x = i + 0.5
    rad = math.acos(x / R)
    y = math.sin(rad) * R
    y_max = int(y - 0.5) + 1
    count = y_max * 2 - 1
    ans += count * 2  # 左右の分を合わせる
    if i == 0:
      ans //= 2

  print(ans)

if __name__ == "__main__":
  main()