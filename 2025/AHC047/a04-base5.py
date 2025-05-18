import os
from typing import Tuple
import random

random.seed(1317)  # 乱数のシードを固定

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

def calc_score(s_list: list, p_list: list, state_list: list, prob_matrix: list) -> int:
  pass  # スコア計算の関数を定義する必要がある

def main():
  _, _, _ = map(int, input().split())  # N, M, Lが与えられるが、固定されているため無視
  s_p_list = [list(input().split()) for _ in range(N)]
  s_list = [""]*N  # 
  p_list = [0]*N
  for i in range(N):
    s, p = s_p_list[i]
    s_list[i] = s
    p_list[i] = int(p)

  # 最も高いスコアを持つ状態と遷移確率行列を見つける
  best_s = ""
  max_p = 0
  for i in range(N):
    s = s_list[i]
    p = p_list[i]
    if p > max_p:
      max_p = p
      best_s = s
  # ic(best_s, max_p)

  state_list = list(best_s) + [random.choice("abcdef") for _ in range(M-len(best_s))]  # 状態のリスト
  ic(state_list)
  prob_matrix = [[5]*M for _ in range(M)]  # 遷移確率行列

  # base_sにほぼ確実に遷移させる
  for i in range(M):
    if i < len(best_s)-1:
      prob_matrix[i][i+1] += 40
    else:
      for j in range(M):
        prob_matrix[i][j] += 3
      # ランダムに4つ+1する
      for j in range(4):
        prob_matrix[i][random.randint(0, M-1)] += 1

  # 得点を計算
  score = calc_score(s_list, p_list, state_list, prob_matrix)
  ic(score)

  for i in range(M):
    print(state_list[i], end=" ")
    print(*prob_matrix[i])

if __name__ == "__main__":
  main()