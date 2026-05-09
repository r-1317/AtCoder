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
  N, K = map(int, input().split())
  a_list = [list(map(int, input().split()))[1:] for _ in range(N)]
  c_list = list(map(int, input().split()))

  k = K

  for i in range(N):
    l = len(a_list[i])
    c = c_list[i]
    if l*c >= k:  # 適切かわからん
      k = (k-1) % l
      print(a_list[i][k])
      sys.exit()
    k -= l*c

if __name__ == "__main__":
  main()