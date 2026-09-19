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

def buy(K, one_cout, k_count, b):  # ドリンクの購入時の支払いの処理
  pay_k = (b - 1) // K + 1  # 多分この式でいけるはず
  b -= pay_k * K
  k_count -= pay_k

  one_cout += -b

  return one_cout, k_count

def main():
  N, M , K = map(int, input().split())
  X, Y = map(int, input().split())
  a_list = list(map(int, input().split()))
  b_list = list(map(int, input().split()))
  a_list.sort()
  b_list.sort()

  a_cum_sum = []
  for i, a in enumerate(a_list):
    if i == 0:
      a_cum_sum.append(a)
    else:
      a_cum_sum.append(a_cum_sum[-1] + a)

  one_cout = X
  k_count = Y
  ans = bisect.bisect_right(a_cum_sum, k_count * K + one_cout)  # 0-indexedを利用したやつ
  if ans is None:
    ans = 0

  ic(ans)
  ic(a_cum_sum)
  ic(a_list)

  for i, b in enumerate(b_list):
    one_cout, k_count = buy(K, one_cout, k_count, b)
    if k_count < 0:
      break

    a_count = bisect.bisect_right(a_cum_sum, k_count * K + one_cout)
    if a_count is None:
      a_count = 0

    ans = max(ans, i + 1 + a_count)

  print(ans)


if __name__ == "__main__":
  main()