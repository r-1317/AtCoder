import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def dist(x1, y1, x2, y2):  # 距離の2乗
  return (x1 - x2)**2 + (y1 - y2)**2

def main():
  T = int(input())

  for _ in range(T):
    x1, y1, r1, x2, y2, r2 = map(int, input().split())
    d = dist(x1, y1, x2, y2)
    r = (r1 + r2)**2

    if  (r1 - r2)**2 <= d <= r:
      print("Yes")
    else:
      print("No")


if __name__ == "__main__":
  main()