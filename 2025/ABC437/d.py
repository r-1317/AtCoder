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
  N, M = map(int, input().split())
  a_list = list(map(int, input().split()))  # 長さN
  b_list = list(map(int, input().split()))  # 長さM
  a_list.sort()
  b_list.sort()
  ic(a_list)
  ic(b_list)

  a_cum_list_l = [0]*N
  a_cum_list_r = [0]*N

  # 左から右へ  lのリストを埋める
  for i in range(N):
    cum_sum = 0 if i == 0 else a_cum_list_l[i-1]
    a_cum_list_l[i] = cum_sum + a_list[i]

  # 右から左へ  rのリストを埋める
  for i in range(N-1, -1, -1):
    cum_sum = 0 if i == N-1 else a_cum_list_r[i+1]
    a_cum_list_r[i] = cum_sum + a_list[i]

  ic(a_cum_list_l)
  ic(a_cum_list_r)

  ans = 0
  idx = 0
  for i in range(M):
    b = b_list[i]
    ic(b)
    # a_list[idx] がb以上になるようにする
    while idx < N and a_list[idx] < b:
      idx += 1
    if idx > 0:
      ans += b*(idx) - a_cum_list_l[idx-1]
      ic(b*(idx) - a_cum_list_l[idx-1])
    if idx < N:
      ans += a_cum_list_r[idx] - b*(N-idx)
      ic(a_cum_list_r[idx] - b*(N-idx))

    ans %= 998244353

  print(ans)

if __name__ == "__main__":
  main()