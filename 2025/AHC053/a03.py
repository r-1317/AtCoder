import os
from typing import Tuple

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 500
M = 50
L = 10**15 - 2*10**12
U = 10**15 + 2*10**12

def main():
  _, _, _, _ = map(int, input().split())

  a_list = []  # i番目のカードの値
  x_list = [0] * N  # i番目のカードが属する山
  stride = (U - L) // 2

  for i in range(M):
    a_list.append(L)
  
  for i in range(N//M - 1):
    for j in range(M):
      a_list.append(stride)
    stride //= 2
    

  ic(len(a_list))
  print(*a_list)

  b_list = list(map(int, input().split()))  # i番目の山の合計値の目標

  sum_list = [0] * M  # i番目の山の合計値

  max_err = a_list[-1] // 2  # 最大誤差

  # x_listを埋める
  for i in range(M):
    x_list[i] = i+1
    sum_list[i] = a_list[i]
  for i in range(1, N//M):
    for j in range(M):
      # 追加しても目標値+最大誤差を超えないなら追加
      if sum_list[j] + a_list[i*M + j] <= b_list[j] + max_err:
        x_list[i*M + j] = j+1
        sum_list[j] += a_list[i*M + j]

  # 出力
  print(*x_list)

if __name__ == "__main__":
  main()