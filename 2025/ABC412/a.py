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
  n = int(input())
  ans = 0

  for _ in range(n):
    a, b = map(int, input().split())
    if a < b:
      ans += 1

  print(ans)

if __name__ == "__main__":
  main()