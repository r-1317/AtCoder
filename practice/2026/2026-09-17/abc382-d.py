import os
from typing import List

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def dfs(N, i, prev_a, rem, ans_list: List[List[int]], current_ans: List[int]):
  if i == N:
    ans_list.append(current_ans)
    return None

  for j in range(rem + 1):
    new_a = prev_a + 10 + j
    new_rem = rem - j
    new_current_ans = current_ans[:]
    new_current_ans.append(new_a)
    dfs(N, i+1, new_a, new_rem, ans_list, new_current_ans)

  return None

def main():
  N, M = list(map(int, input().split()))
  rem = M - (N * 10 - 9)
  ic(rem)

  ans_list: List[List[int]] = []
  dfs(N, 0, -9, rem, ans_list, [])

  ans_list.sort()
  print(len(ans_list))
  for ans in ans_list:
    for a in ans:
      print(a, end=" ")
    print()

if __name__ == "__main__":
  main()