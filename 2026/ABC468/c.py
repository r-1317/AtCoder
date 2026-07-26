import os

import itertools

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
  p_list = list(input().split())
  p_str = ""
  for c in p_list:
    p_str += str(int(c) - 1)
  P = int(p_str)
  q_list = list(input().split())
  q_str = ""
  for c in q_list:
    q_str += str(int(c) - 1)
  Q = int(q_str)
  ic(P, Q)

  ans = 0

  for touple_x in itertools.permutations("0123456789"[:N], N):
    x_str = ""
    for c in touple_x:
      x_str += c
    x = int(x_str)
    if P < x < Q:
      ans += 1
      ic(x)

  print(ans)

if __name__ == "__main__":
  main()