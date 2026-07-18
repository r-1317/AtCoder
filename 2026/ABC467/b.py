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
  N = int(input())

  ans = 0

  for _ in range(N):
    a, b, s = input().split()
    a = int(a)
    b = int(b)

    if s == "keep":
      ans += b - a

  print(ans)

if __name__ == "__main__":
  main()