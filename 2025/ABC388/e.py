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

  exist_list = [True] * n

  ans = 0

  for i in range(n):
    if not exist_list[i]:
      continue
    a = a_list[i]
    b_index = bisect.bisect_left(a_list, a*2)
    if b_index == n:
      break
    while not exist_list[b_index]:
      b_index += 1
      if b_index == n:
        break
    if b_index == n:
      break
    exist_list[b_index] = False
    ans += 1

  print(ans)

if __name__ == "__main__":
  main()