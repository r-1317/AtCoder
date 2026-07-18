import os
# from sympy import geometry

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def is_collinear(p1, p2, p3):
  x1, y1 = p1
  x2, y2 = p2
  x3, y3 = p3
  return (x3 - x1) * (y2 - y1) == (x2 - x1) * (y3 - y1)

def main():
  T = int(input())

  for _ in range(T):
    px, py, qx, qy, rx, ry, sx, sy = map(int, input().split())
    dx1 = qx - px
    dy1 = qy - py
    dx2 = sx - rx
    dy2 = sy - ry

    dx3 = rx - px
    dy3 = ry - py
    dx4 = sx - px
    dy4 = sy - py


    p = (px, py)
    q = (qx, qy)
    r = (rx, ry)
    s = (sx, sy)

    if MyPC and px == 2:
      ic(dx1, dy1, dx2, dy2)

    if not(dx1 * dy2 == dy1 * dx2):
      print("Yes")
      continue

    if is_collinear(p, q, r) and is_collinear(p, q, s):
      print("Yes")
      continue

    print("No")

if __name__ == "__main__":
  main()