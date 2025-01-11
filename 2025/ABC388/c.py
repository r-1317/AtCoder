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
  n = int(input())
  a_list = list(map(int, input().split()))

  ans = 0

  for a in a_list:
    ans += bisect.bisect(a_list, a//2)
    ic(bisect.bisect(a_list, a//2))

  print(ans)

if __name__ == "__main__":
  main()