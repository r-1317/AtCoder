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
  N, Q = map(int, input().split())
  a_list = list(map(int, input().split()))

  double_a_list = a_list + a_list
  cum_sum_list = [0] * (2*N + 1)

  for i in range(2*N):
    cum_sum_list[i+1] = cum_sum_list[i] + double_a_list[i]

  head = 0

  for _ in range(Q):
    query = list(map(int, input().split()))
    t = query[0]

    if t == 1:
      c = query[1]
      head = (head + c) % N
    elif t == 2:
      l, r = query[1], query[2]
      l -= 1
      r -= 1

      s = cum_sum_list[head + r + 1] - cum_sum_list[head + l]
      print(s)
      ic(s)

if __name__ == "__main__":
  main()