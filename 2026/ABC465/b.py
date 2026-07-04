import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  X, Y, L, R, A, B = map(int, input().split())

  ans = 0

  for i in range(A, B):
    if L <= i <= R - 1:
      ans += X
    else:
      ans += Y

  print(ans)

if __name__ == "__main__":
  main()