import os
import sys

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
  a_list = list(map(int, input().split()))
  b_list = list(map(int, input().split()))
  a_list.sort()
  b_list.sort()

  ans = 0
  idx = 0
  for b in b_list:
    while idx < N and a_list[idx] < b:
      idx += 1
    if idx >= N:
      print(-1)
      sys.exit()
    ans += a_list[idx]
    idx += 1
  print(ans)

if __name__ == "__main__":
  main()