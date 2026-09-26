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
  Q = int(input())
  S = input()
  T = input()

  idx_list = [-1]
  for i in range(len(S) - len(T) + 1):
    if S[i: i + len(T)] == T:
      idx_list.append(i + 1)
  idx_list.append(10**9)

  for _ in range(Q):
    l, r = map(int, input().split())
    a_idx = bisect.bisect_left(idx_list, l)
    a = idx_list[a_idx]
    if a + len(T) - 1 <= r:
      print("Yes")
    else:
      print("No")


if __name__ == "__main__":
  main()