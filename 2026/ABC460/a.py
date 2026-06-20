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
  N, M = map(int, input().split())

  x = M
  ans = 0

  while x != 0:
    x = N % x
    ans += 1

  print(ans)

if __name__ == "__main__":
  main()