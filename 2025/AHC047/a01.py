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

  state_list = ["a", "b", "c", "d", "e", "f", "a", "b", "c", "d", "e", "f"]  # 状態のリスト
  prob_matrix = [[9]*4+[8]*(M-4) for _ in range(M)]  # 遷移確率行列

  # 得点を計算
  score = calc_score(s_list, p_list, state_list, prob_matrix)
  ic(score)

  for i in range(M):
    print(state_list[i], end=" ")
    print(*prob_matrix[i])

if __name__ == "__main__":
  main()