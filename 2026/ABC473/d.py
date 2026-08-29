import os
from typing import List

# MyPC = os.path.basename(__file__) != "Main.py"
# if MyPC:
#   from icecream import ic
#   ic.disable()
# else:
#   def ic(*args):
#     return None

# ic.enable() if MyPC else None

def saiki(N: int, K: int, ans_list: List[List[int]], arr: List[int], x: int, i: int):
  if i == 0:
    if x == K:
      ans_list.append(arr[::-1])
    return None

  if i == 1:
    j = K - x
    new_arr = arr[:] + [j]
    saiki(N, K, ans_list, new_arr, x + j*i, i - 1)
    return None

  j = 0
  while x + j*i <= K and len(ans_list) <= 3*10**5:
    new_arr = arr[:] + [j]
    saiki(N, K, ans_list, new_arr, x + j*i, i - 1)
    j += 1
  return None


def main():
  N, K = list(map(int, input().split()))
  ans_list = []
  saiki(N, K, ans_list, [], 0, N)

  ans_list.sort()

  for ans in ans_list:
    for a in ans:
      print(a, end = " ")
    print()

if __name__ == "__main__":
  main()