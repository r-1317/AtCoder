import os
import sys
import math

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# https://qiita.com/fault/items/547cb36153df35cefa8a のコードを改変
def solv_quadratic_equation(a, b, c):
  """ 2次方程式を解く  """
  if b**2 < 4*a*c:
    return -1
  D = math.isqrt(b**2 - 4*a*c)
  x_1 = (-b + D) // (2 * a)
  x_2 = (-b - D) // (2 * a)
  
  # return x_1, x_2
  return max(x_1, x_2)

def main():
  N = int(input())

  for d in range(1, 10**6 + 1):
    a = 3 * d
    b = 3 * d**2
    c = d**3 - N
    k = solv_quadratic_equation(a, b, c)
    if (k + d)**3 - k**3 == N and k > 0:
      print(k + d, k)
      sys.exit()

  print(-1)

if __name__ == "__main__":
  main()