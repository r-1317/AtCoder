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
  N, Q = map(int, input().split())
  a_list = list(map(int, input().split()))
  a_list.sort()
  for _ in range(Q):
    X, Y = map(int, input().split())

    while True:
      x_idx = bisect.bisect_left(a_list, X)
      y_idx = bisect.bisect(a_list, X+Y-1)
      diff = y_idx - x_idx
      z = X + Y + diff - 1
      ic(z)
      z_idx = bisect.bisect(a_list, z-1)
      ic(x_idx)
      ic(y_idx)
      ic(z_idx)
      new_y_idx = bisect.bisect_left(a_list, X+Y-1)
      ic(new_y_idx)
      if new_y_idx == z_idx:
        break
      X = X + Y
      Y = z_idx - new_y_idx
    if z_idx < N and a_list[z_idx] == z:
      z += 1
    ic(z)
    print(z)

if __name__ == "__main__":
  main()