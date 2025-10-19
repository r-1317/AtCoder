import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def f(c, dd):
  return int(str(c) + str(dd))

def main():
  T = int(input())

  for _ in range(T):
    c, d = map(int, input().split())

    min_z = f(c, c+1)
    max_z = f(c, c+d)

    min_jk = 0
    max_jk = 0

    current_jk = 2**60
    stride = 2**59
    while stride:
      current_z = current_jk**2
      if current_z < min_z:
        current_jk += stride
      elif min_z < current_jk:
        current_jk -= stride
      stride //= 2
    min_jk = current_jk

    current_jk = 2**60
    stride = 2**59
    while stride:
      current_z = current_jk**2
      if current_z < max_z:
        current_jk += stride
      elif max_z < current_z:
        current_jk -= stride
      stride //= 2
    max_jk = current_jk

    ans = max_jk - min_jk + 1
    ic(min_jk, max_jk)
    ic(ans)
    print(ans)

if __name__ == "__main__":
  main()