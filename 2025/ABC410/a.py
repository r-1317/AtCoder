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
  a_list = list(map(int, input().split()))
  k = int(input())

  ans = 0

  for a in a_list:
    if k <= a:
      ans += 1

  print(ans)


if __name__ == "__main__":
  main()