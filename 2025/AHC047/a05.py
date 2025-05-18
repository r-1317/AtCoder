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
  X = 4
  Y = 3
  # 遷移確率をランダムにX%を付け替える。これを列ごとにY回行う。
  for i in range(M):
    for _ in range(Y):
      # ランダムに2つの列を選ぶ
      j = random.randint(0, M-1)
      k = random.randint(0, M-1)
      if prob_matrix[i][j] < X:  # X%未満の確率は変更しない
        continue
      # 確率を変更
      prob_matrix[i][j] -= X
      prob_matrix[i][k] += X
  return prob_matrix


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

  # 遷移確率行列の初期化
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

  # ここまでが遷移確率行列の初期化
  # ここからが行列の微調整

  # 得点を計算
  max_score = calc_score(s_list, p_list, state_list, prob_matrix)
  ic(max_score)
  # 出力
  for i in range(M):
    print(state_list[i], end=" ")
    print(*prob_matrix[i])

  # 1.5秒が経過するまで山登り
  while time.time() - start_time < 1.5:
    # ランダムに遷移確率を変更
    next_prob_matrix = random_change(prob_matrix[:])
    # 得点を計算
    next_score = calc_score(s_list, p_list, state_list, next_prob_matrix)
    # スコアが上がったら更新
    if next_score > max_score:
      ic(next_score)
      max_score = next_score
      prob_matrix = next_prob_matrix[:]
      # 出力
      for i in range(M):
        print(state_list[i], end=" ")
        print(*prob_matrix[i])

if __name__ == "__main__":
  main()