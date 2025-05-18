import os
from typing import Tuple
import random

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 36
M = 12
L = 10**6
PADDING = [9]*4+[8]*(M-4)  # 使わない状態の確率遷移行列の初期値

def main():
  _, _, _ = map(int, input().split())  # N, M, Lが与えられるが、固定されているため無視
  s_p_list = [list(input().split()) for _ in range(N)]
  s_list = [""]*N  # 
  p_list = [0]*N
  for i in range(N):
    s, p = s_p_list[i]
    s_list[i] = s
    p_list[i] = int(p)

  state_list = ["a", "b", "c", "d", "e", "f", "a", "b", "c", "d", "e", "f"]  # 状態のリスト
  prob_matrix = [[0]*M for _ in range(6)] + [PADDING for _ in range(M-6)]  # 遷移確率行列

  transition_point_list = [[0]*6 for _ in range(6)]  # 文字ごとの遷移ポイント(これの比率で遷移する)
  
  # 遷移確率を加算
  for i in range(N):
    s = s_list[i]
    p = p_list[i]
    tmp_len = len(s)
    for j in range(tmp_len-1):
      s1_index = ord(s[j]) - ord("a")
      s2_index = ord(s[j+1]) - ord("a")
      transition_point_list[s1_index][s2_index] += p/tmp_len
  ic(transition_point_list)

  # 遷移確率行列の作成
  transition_point_sum_list = [0]*6  # 各行の合計
  for i in range(6):
    for j in range(6):
      transition_point_sum_list[i] += transition_point_list[i][j]

  # 各行の合計で割り、100を掛け、少数点以下を切り捨てたものをprob_matrixに格納
  for i in range(6):
    for j in range(6):
      if transition_point_sum_list[i] != 0:  # 0はほとんどないが、念のため
        prob_matrix[i][j] = transition_point_list[i][j] / transition_point_sum_list[i]
        prob_matrix[i][j] = int(prob_matrix[i][j] * 100)
      else:
        prob_matrix[i][j] = 0

  # 各行の合計と100の差を計算
  diff_list = [0]*6
  for i in range(6):
    diff_list[i] = 100 - sum(prob_matrix[i])
  ic(diff_list)
  # 各行の合計と100の差をランダムに分配
  for i in range(6):
    for _ in range(diff_list[i]):
      j = random.randint(0, 5)
      prob_matrix[i][j] += 1

  # 出力
  for i in range(M):
    print(state_list[i], end=" ")
    print(*prob_matrix[i])

if __name__ == "__main__":
  main()