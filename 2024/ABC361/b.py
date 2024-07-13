import os
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  a, b, c, d, e, f = map(int, input().split())  # 直方体の対角線上の2点(a,b,c)と(d,e,f)
  g, h, i, j, k, l = map(int, input().split())  # 直方体の対角線上の2点(g,h,i)と(j,k,l)

  ans = False

  if not((j <= a or d <= g) or (k <= b or e <= h) or (l <= c or f <= i)):
    ans = True

  print("Yes" if ans else "No")

if __name__ == "__main__":
  main()