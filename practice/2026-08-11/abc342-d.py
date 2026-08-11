import os
import math

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def calc_d(a):
  d = -1
  for i in range(1, 1000):
    if i**2 > a:
      break
    if a % i**2 == 0:
      d = i

  return a // d**2

def main():
  N = int(input())
  a_list = list(map(int, input().split()))

  d_list = [0]*N
  for i, a in enumerate(a_list):
    if a == 0:
      continue
    d = calc_d(a)
    d_list[i] = d

  count_list = [0]*10**6

  for d in d_list:
    count_list[d] += 1

  ans = 0

  # 0のぶんを先に出す
  ans += count_list[0] * (N - count_list[0])

  for i, c in enumerate(count_list):
    # if i == 0:  # これ要らんの?
    #   continue
    ans += c * (c - 1) // 2

  ic(d_list)
  ic(count_list[:10])
  print(ans)


if __name__ == "__main__":
  main()