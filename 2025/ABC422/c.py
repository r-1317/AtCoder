import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def f(x, na, nb, nc):
  na -= x
  nc -= x
  res = na + nb + nc
  # ic(x, na, nb, nc, res)
  if na < 0 or nc < 0 or res < x:
    return False
  
  return True

def main():
  T = int(input())
  for _ in range(T):
    na, nb, nc = map(int, input().split())
    # 二分探索
    x = 2**29
    stride = 2**28
    while 0 < stride:
      if f(x, na, nb, nc):
        x += stride
        # ic(x)
      else:
        x -= stride
        # ic(x)
      stride //= 2

    # 誤差調整
    if not f(x, na, nb, nc):
      x -= 1

    ic(x)
    print(x)

if __name__ == "__main__":
  main()