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
  N = int(input())
  S = input()
  s_list = [-1] + [int(c) for c in S]
  c_list = list(map(int, input().split()))

  # 実装の都合で1-indexedにする
  cum_sum_even = [0]  # 0101...
  cum_sum_odd = [0]  # 1010...

  for i in range(1, N+1):
    cum_sum_even.append(cum_sum_even[-1])
    if s_list[i] != i % 2:# 偶数で追加のコストがいる場合
      cum_sum_even[-1] += c_list[i-1]
    cum_sum_odd.append(cum_sum_odd[-1])
    if s_list[i] == i % 2:  # 奇数で追加のコストがいる場合
      cum_sum_odd[-1] += c_list[i-1]

  ic(cum_sum_even)
  ic(cum_sum_odd)

  ans = 10**18

  for i in range(1, N):
    # 偶数->奇数の場合
    current_ans = cum_sum_even[i] + cum_sum_odd[-1] - cum_sum_odd[i]
    ans = min(ans, current_ans)
    # 偶数->奇数の場合
    current_ans = cum_sum_odd[i] + cum_sum_even[-1] - cum_sum_even[i]
    ans = min(ans, current_ans)

  print(ans)

if __name__ == "__main__":
  main()