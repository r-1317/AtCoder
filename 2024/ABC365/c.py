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


def calc_cost(a_list, x):
  cost = 0
  for a in a_list:
    cost += min(x, a)
  return cost

def main():
  n, m = map(int, input().split())
  a_list = list(map(int, input().split()))

  if sum(a_list) <= m:
    print("infinite")
    sys.exit()

  # 二分探索

  x = 10**9 // 2
  x_diff = x

  while True:
    cost = calc_cost(a_list, x)
    ic(x, cost)

    if m == cost:
      break

    elif m < cost:
      x -= x_diff // 2
      x_diff = x_diff // 2

    else:
      x += x_diff // 2
      x_diff = x_diff // 2

    ic(x, x_diff)

    if x_diff == 0:
      break

  ic("二分探索終了")
  
  # 予算よりも大きい場合
  if m < cost:
    while True:
      x -= 1
      cost = calc_cost(a_list, x)
      ic(x, cost)
      if cost <= m:
        break
  # 予算よりも小さい場合
  elif cost < m:
    while calc_cost(a_list, x+1) <= m:
      x += 1
      ic(x, cost)

  print(x)



if __name__ == "__main__":
  main()