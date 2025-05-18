import os
from typing import List, Dict, Tuple
import random
import time

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
PADDING = [9]*4 + [8]*(M-4)  # 使わない状態の確率遷移行列の初期値
ALPHA = 'abcdef'
ALPHA_IDX = {c: i for i, c in enumerate(ALPHA)}

def build_kmp_next(pat: str) -> List[List[int]]:
  """next[k][c] = progress after reading c when we are at prefix length k."""
  m = len(pat)
  nxt = [[0]*6 for _ in range(m+1)]
  for k in range(m+1):
    for ci, ch in enumerate(ALPHA):
      # longest l (<=m) s.t. pat[:l] is suffix of pat[:k]+ch
      l = min(m, k+1)
      while l and pat[:l] != (pat[:k]+ch)[-l:]:
        l -= 1
      nxt[k][ci] = l
  return nxt

def vec_mul(v: List[float], T: List[Dict[int, float]]) -> List[float]:
  n = len(v)
  nv = [0.0]*n
  for i, vi in enumerate(v):
    if vi == 0.0:
      continue
    for j, pij in T[i].items():
      nv[j] += vi * pij
  return nv

def mat_mul(A: List[Dict[int, float]], B: List[Dict[int, float]]) -> List[Dict[int, float]]:
  n = len(A)
  C = [dict() for _ in range(n)]
  for i in range(n):
    for k, aik in A[i].items():
      for j, bkj in B[k].items():
        C[i][j] = C[i].get(j, 0.0) + aik * bkj
  return C

def  build_transition(pat: str,
                      state_list: List[str],
                      prob_matrix: List[List[int]]) -> Tuple[List[Dict[int, float]], List[float]]:
  """未ヒット状態のみで作る疎行列 T_i と初期ベクトル v0 を返す。"""
  m = len(pat)
  nxt = build_kmp_next(pat)
  size = m * M
  T = [dict() for _ in range(size)]

  for prog in range(m):
    for s in range(M):
      fr = prog*M + s
      for t in range(M):
        p = prob_matrix[s][t] / 100.0
        if p == 0.0:
          continue
        ch = state_list[t]
        np = nxt[prog][ALPHA_IDX[ch]]
        if np == m:
          continue
        to = np*M + t
        T[fr][to] = T[fr].get(to, 0.0) + p

  first_prog = nxt[0][ALPHA_IDX[state_list[0]]]
  if first_prog == m:
    return T, None
  v0 = [0.0]*size
  v0[first_prog*M + 0] = 1.0
  return T, v0

def power_vector(v: List[float], T: List[Dict[int, float]], steps: int) -> float:
  """v * T^steps を計算し、要素和（＝未ヒット確率）を返す。"""
  if steps == 0:
    return sum(v)
  mats = [T]
  k = 0
  while (1 << (k+1)) <= steps:
    mats.append(mat_mul(mats[k], mats[k]))
    k += 1
  idx = 0
  while steps:
    if steps & 1:
      v = vec_mul(v, mats[idx])
    steps >>= 1
    idx += 1
  return sum(v)

def  calc_score(s_list: List[str],
                p_list: List[int],
                state_list: List[str],
                prob_matrix: List[List[int]]) -> int:
  total = 0.0
  rem_steps = L - 1
  for pat, P in zip(s_list, p_list):
    T, v0 = build_transition(pat, state_list, prob_matrix)
    if v0 is None:
      Qi = 1.0
    else:
      nohit = power_vector(v0, T, rem_steps)
      Qi = 1.0 - nohit
    total += P * Qi
  return round(total)

def random_change(prob_matrix: List[List[int]]) -> List[List[int]]:
  # 遷移確率をランダムに10%付け替える。これを列ごとに
  pass

def main():
  start_time = time.time()  # 計測開始
  _, _, _ = map(int, input().split())  # N, M, Lが与えられるが、固定されているため無視
  s_p_list = [list(input().split()) for _ in range(N)]
  s_list = [""]*N  # 
  p_list = [0]*N
  for i in range(N):
    s, p = s_p_list[i]
    s_list[i] = s
    p_list[i] = int(p)

  state_list = ["a", "b", "c", "d", "e", "f", "a", "b", "c", "d", "e", "f"]  # 状態のリスト
  prob_matrix = [PADDING[:] for _ in range(M)]  # 遷移確率行列

  # 遷移確率行列の初期化
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
  # ic(transition_point_list)

  # 遷移確率行列の作成
  transition_point_sum_list = [0]*6  # 各行の合計
  for i in range(6):
    for j in range(6):
      transition_point_sum_list[i] += transition_point_list[i][j]

  # 各行の合計で割り、100を掛け、半分にしたもの(=50をかけた)の少数点以下を切り捨てたものををprob_matrixに格納
  for i in range(6):
    for j in range(6):
      if transition_point_sum_list[i] != 0:  # 0はほとんどないが、念のため
        prob_matrix[i][j] = transition_point_list[i][j] / transition_point_sum_list[i]
        prob_matrix[i][j] = int(prob_matrix[i][j] * 50)
        prob_matrix[i][j+6] = prob_matrix[i][j]
  ic(prob_matrix)

  # 各行の合計と100の差を計算
  diff_list = [0]*6
  for i in range(6):
    diff_list[i] = 100 - sum(prob_matrix[i])
  ic(diff_list)
  # 各行の合計と100の差をランダムに分配
  for i in range(6):
    for _ in range(diff_list[i]):
      j = random.randint(0, M-1)
      prob_matrix[i][j] += 1

  # 遷移確率行列の上半分を下半分にコピー
  for i in range(6):
    prob_matrix[i+6] = prob_matrix[i][:]
  ic(prob_matrix)

  # ここまでで遷移確率行列の初期化が完了
  # 得点の計算
  max_score = calc_score(s_list, p_list, state_list, prob_matrix)
  ic(max_score)
  # ここからは遷移確率行列の山登り
  while time.time() - start_time < 1.5:  # 制限時間1.5秒
    next_prob_matrix = random_change(prob_matrix)
    next_score = calc_score(s_list, p_list, state_list, next_prob_matrix)


  # 出力
  for i in range(M):
    print(state_list[i], end=" ")
    print(*prob_matrix[i])

if __name__ == "__main__":
  main()