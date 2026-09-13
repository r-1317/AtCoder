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
  N, S, L = map(int, input().split())
  a_list = list(map(int, input().split()))

  S -= 1

  cum_sum_list = [0]
  for a in a_list:
    cum_sum_list.append(cum_sum_list[-1] + a)
  ic(cum_sum_list)

  max_count = 0
  for i in range(N):  # 目的地1
    for j in range(N):  # 目的地2
      len = cum_sum_list[max(S, i)] - cum_sum_list[min(S, i)]
      len += cum_sum_list[max(i, j)] - cum_sum_list[min(i, j)]
      if len > L:
        continue
      count = max(S, i, j) - min(S, i, j) + 1
      max_count = max(max_count, count)

  print(max_count)


if __name__ == "__main__":
  main()