import os
import math
from typing import Tuple
import sys

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

C = 34  # 二分探索用カードの枚数

def main():
  _, _, _, _ = map(int, input().split())

  a_list = []  # i番目のカードの値
  x_list = [0] * N  # i番目のカードが属する山
  stride = (U - L) // 2

  for i in range(M):
    a_list.append(L)

  while True:
    for j in range(C):
      a_list.append(stride)
      if len(a_list) == N:
        break
    stride //= 2
    if len(a_list) == N:
      break

  # ic(len(a_list))
  print(*a_list)

  b_list = list(map(int, input().split()))  # i番目の山の合計値の目標

  sum_list = [0] * M  # i番目の山の合計値

  max_err = a_list[-1] // 2  # 最大誤差

  # x_listを埋める
  for i in range(M):
    x_list[i] = i+1
    sum_list[i] = a_list[i]
  for i in range((N-M)//C + 1):
    count = 0
    for j in range(M):
      if M + i*C + count >= N or count >= C:
        break
      # 追加しても目標値+最大誤差を超えないなら追加
      if sum_list[j] + a_list[M + i*C + count] <= b_list[j] + max_err:
        x_list[M + i*C + count] = j+1
        sum_list[j] += a_list[M + i*C + count]
        count += 1

  # 出力
  print(*x_list)

  # スコア計算
  if MyPC:
    # S_j: 各山の合計値, b_list: 目標値
    E = 0
    for j in range(M):
      E += abs(sum_list[j] - b_list[j])
    score = round((20 - (0 if E == 0 else (math.log10(1 + E)))) * 5 * 10**7)
    print(score, file=sys.stderr)

if __name__ == "__main__":
  main()