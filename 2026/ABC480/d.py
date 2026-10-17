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
  N, Q = map(int, input().split())
  a_list = list(map(int, input().split()))

  cum_sum_list = [0]  # この0のぶんだけindexが1つずれる
  for a in a_list:
    cum_sum_list.append(cum_sum_list[-1] + a)

  cum_sum_2D = [0]  # 累積和の累積和
  for c in cum_sum_list:
    cum_sum_2D.append(cum_sum_2D[-1] + c)
  cum_sum_2D = cum_sum_2D[1:]  # 0が2つ続くので片方を削除

  size_list = [1]  # これも累積和。ただindexがずれないやつ
  for i in range(2, N + 1):
    size_list.append(size_list[-1] + i)

  ic(cum_sum_list)
  ic(cum_sum_2D)
  ic(size_list)

  for _ in range(Q):
    l, r = (map(int, input().split()))  # これは1-indexedなので注意
    ans = 0
    chunk_idx = bisect.bisect_right(size_list, r) - 1
    chunk_size = size_list[chunk_idx]
    ans += cum_sum_2D[chunk_idx + 1]
    r -= chunk_size
    ans += cum_sum_list[r]

    d = 0  # 引くやつ
    l -= 1
    if l != 0:
      chunk_idx_2 = bisect.bisect_right(size_list, l) - 1
      chunk_size_2 = size_list[chunk_idx_2]
      d += cum_sum_2D[chunk_idx_2 + 1]
      l -= chunk_size_2
      d += cum_sum_list[l]

    ans -= d
    print(ans)


if __name__ == "__main__":
  main()