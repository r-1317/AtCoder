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
  N, M, K = map(int, input().split())

  L = math.lcm(N, M)

  x = 2**60
  stride = 2**59

  ic(N, M, L)

  while stride > 0:
    count = x // N + x // M - 2 * (x // L)
    ic(count)
    if count < K:
      x += stride
    elif count > K or ((x-1) // N + (x-1) // M - 2 * ((x-1) // L)) == count:
      x -= stride

    stride //= 2

  print(x)


if __name__ == "__main__":
  main()