import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  n, l = map(int, input().split())
  d_list = list(map(int, input().split()))

  # 3倍する
  one_third_l = l
  l *= 3
  d_list = [d * 3 for d in d_list]

  position_list = [0] * n
  cum_sum_list = [0] * n

  for i in range(1, n):
    cum_sum_list[i] = cum_sum_list[i - 1] + d_list[i - 1]

  for i in range(n):
    position_list[i] = cum_sum_list[i] % l
  ic(position_list)

  points_num_list = [0] * l

  for i in range(n):
    points_num_list[position_list[i]] += 1
  ic(points_num_list)

  ans = 0


  for i in range(one_third_l):
    ans += points_num_list[i] * points_num_list[i + one_third_l] * points_num_list[i + 2 * one_third_l]

  ic(ans)
  print(ans)



if __name__ == "__main__":
  main()