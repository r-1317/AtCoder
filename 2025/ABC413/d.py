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

def main():
  t = int(input())
  for _ in range(t):
    n = int(input())
    a_list = list(map(int, input().split()))

    a = a_list[0]
    b = -a
    a_count = a_list.count(a)
    b_count = a_list.count(b)
    half_n_floor = n // 2
    half_n_ceil = (n + 1) // 2
    if (a_count == half_n_floor and b_count == half_n_ceil) or (a_count == half_n_ceil and b_count == half_n_floor):
      ic("Yes")
      print("Yes")
      continue
    elif a_count == n:
      ic("Yes")
      print("Yes")
      continue

    # 絶対値でソート
    a_list.sort(key=abs, reverse=True)
    ic(a_list)

    flag = True

    for i in range(n-2):
      if a_list[i] * a_list[i + 2] != a_list[i + 1] * a_list[i + 1]:
        flag = False
        break

    if flag:
      ic("Yes")
      print("Yes")
    else:
      ic("No")
      print("No")

if __name__ == "__main__":
  main()