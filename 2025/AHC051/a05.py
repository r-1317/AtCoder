import os
from typing import Tuple
import random
import time
import sys
import math

start_time = time.time()

INLET = (0, 5000)  # 搬入口の座標
MAX_X = 5  # 分別器をつなげる数
TIME_LIMIT = 1.7  # 秒

random.seed(1317)

MyPC = os.path.basename(__file__) != "Main.py"
# MyPC = False
if MyPC:  
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def sign(x: int) -> int:
  return 1 if x > 0 else -1 if x < 0 else 0

def orientation(a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int]) -> int:
  cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
  return sign(cross)

def segments_intersect(p1: Tuple[int, int], p2: Tuple[int, int], q1: Tuple[int, int], q2: Tuple[int, int]) -> bool:
  if (max(p1[0], p2[0]) < min(q1[0], q2[0]) or
    max(q1[0], q2[0]) < min(p1[0], p2[0]) or
    max(p1[1], p2[1]) < min(q1[1], q2[1]) or
    max(q1[1], q2[1]) < min(p1[1], p2[1])):
    return False
  o1 = orientation(p1, p2, q1)
  o2 = orientation(p1, p2, q2)
  o3 = orientation(q1, q2, p1)
  o4 = orientation(q1, q2, p2)
  return (o1 * o2 < 0) and (o3 * o4 < 0)

# サンプルの出力関数
def sample_ans(N: int, M: int, K: int, processor_positions: list, sorter_positions: list, prob: list) -> None:
  # i番の位置にi番の処理装置を設置
  proc_assign = ' '.join(str(i) for i in range(N))
  # 搬入口 (0,5000) と最も近い設置場所を結ぶ
  inlet = (0, 5000)
  dist_sq = [((x - inlet[0])**2 + (y - inlet[1])**2, i) for i, (x, y) in enumerate(sorter_positions)]
  _, nearest_i = min(dist_sq)
  inlet_conn = N + nearest_i

  # 0番の分別器を設置し、出口1を一番確率の高いごみ種の処理装置と、出口2を一番確率の低いごみ種の処理装置と結ぶ
  first_row = prob[0]
  imax = first_row.index(max(first_row))
  imin = first_row.index(min(first_row))
  sorter_assigns = []
  for i in range(M):
    if i == nearest_i:
      sorter_assigns.append(f"0 {imax} {imin}")
    else:
      sorter_assigns.append("-1")

  print(proc_assign)
  print(inlet_conn)
  print("\n".join(sorter_assigns))

# スコア計算関数
def calc_score(N: int, M: int, K: int, graph: list, prob_list: list, sorter_id_list: list, processor_list: list) -> float:
  """
  各ごみ種類が正しい処理装置に到達する確率を計算し、絶対スコアを返す
  
  Args:
    N: ごみの種類数
    M: 分別器設置場所数
    K: 分別器種類数
    graph: グラフ構造 (隣接リスト) [処理装置(N個), 分別器(M個), 搬入口(1個)]
    prob_list: 各分別器種類の各ごみ種類に対する出口1への確率
    sorter_id_list: 各分別器設置場所に設置された分別器の種類ID (-1は未設置)
    processor_list: 各処理装置設置場所に設置された処理装置の種類ID
  
  Returns:
    絶対スコア
  """
  
  # 各ごみ種類が各ノードに到達する確率を計算
  # prob[waste_type][node_id] = ごみ種類waste_typeがnode_idに到達する確率
  prob = [[0.0] * (N + M + 1) for _ in range(N)]
  
  # 搬入口(最後のノード)からスタート
  inlet_node = N + M
  for waste_type in range(N):
    prob[waste_type][inlet_node] = 1.0
  
  # トポロジカルソートを行いつつ確率を計算
  # 搬入口から開始してBFSで探索
  from collections import deque
  
  for waste_type in range(N):
    queue = deque([inlet_node])
    visited = set()
    
    while queue:
      current = queue.popleft()
      if current in visited:
        continue
      visited.add(current)
      
      current_prob = prob[waste_type][current]
      if current_prob == 0:
        continue
      
      # 搬入口の場合
      if current == inlet_node:
        if isinstance(graph[current], int):
          next_node = graph[current]
          prob[waste_type][next_node] += current_prob
          queue.append(next_node)
      
      # 分別器の場合
      elif current >= N:  # 分別器ノード
        sorter_idx = current - N
        sorter_type = sorter_id_list[sorter_idx]
        
        if sorter_type != -1 and len(graph[current]) >= 2:
          # 出口1への確率
          p1 = prob_list[sorter_type][waste_type]
          # 出口2への確率
          p2 = 1.0 - p1
          
          # 出口1への接続先
          next1 = graph[current][0]
          prob[waste_type][next1] += current_prob * p1
          queue.append(next1)
          
          # 出口2への接続先
          next2 = graph[current][1]
          prob[waste_type][next2] += current_prob * p2
          queue.append(next2)
      
      # 処理装置の場合は終点なので何もしない
  
  # 各ごみ種類が正しい処理装置に到達する確率を計算
  correct_probs = []
  for waste_type in range(N):
    correct_prob = 0.0
    for processor_idx in range(N):
      if processor_list[processor_idx] == waste_type:
        correct_prob += prob[waste_type][processor_idx]
    correct_probs.append(correct_prob)
  
  # 絶対スコアを計算
  error_sum = sum(1 - p for p in correct_probs)
  absolute_score = round(10**9 * error_sum / N)
  
  return absolute_score

def main():
  N, M, K = map(int, input().split())  # N: ゴミの種類の数であり処理装置の数, M: 分別器の数, K: 分別器の種類の数
  d_coord_list = [tuple(map(int, input().split())) for _ in range(N)]  # 処理装置予定地の座標
  s_coord_list = [tuple(map(int, input().split())) for _ in range(M)]  # 分別器の予定地の座標

  prob_list = [list(map(float, input().split())) for _ in range(K)]  # 各分別器のゴミiの転送確率

  X = min(MAX_X, N-1)  # 分別器の数はN以下に制限

  processor_id_list = list(range(N))
  sorter_id_list = [-1] * M
  processor_list = list(range(N))  # 処理装置は順番通りに配置

  graph = [[] for _ in range(N+M+1)]  # [処理装置(N個), 分別器(M個), 搬入口(1個)]の順

  # # 各ゴミに対して、最も高確率で転送できる分別器を見つける
  # best_sorters = [-1] * N
  # for i in range(N):
  #   best_prob = 0
  #   for j in range(K):
  #     prob = prob_list[j][i]
  #     if prob > best_prob:
  #       best_prob = prob
  #       best_sorters[i] = j

  # ic(best_sorters)

  # スコアが最も小さくなる分別器の組み合わせ
  best_sorters = [-1] * N

  # 分別器の予定地をランダムにN-1個選び、接続が可能なら採用
  while time.time() - start_time < TIME_LIMIT:
    # tmp_sorter_list = random.sample(range(M), N-1)  # M個の分別器予定地からN-1個をランダムに選ぶ
    tmp_sorter_list = random.sample(range(M), X)  # M個の分別器予定地からX個をランダムに選ぶ

    edge_list = []
    edge_list.append((INLET, s_coord_list[tmp_sorter_list[0]]))  # 搬入口から最初の分別器へ接続
    for i in range(X):
      edge_list.append((s_coord_list[tmp_sorter_list[i]], d_coord_list[i]))
      if i < X-1:
        edge_list.append((s_coord_list[tmp_sorter_list[i]], s_coord_list[tmp_sorter_list[i+1]]))  # 分別器同士を接続
      else:
        edge_list.append((s_coord_list[tmp_sorter_list[i]], d_coord_list[i+1]))  # 最後の分別器から最後の処理装置へ接続

    valid = True

    for i in range(len(edge_list)):
      for j in range(i + 1, len(edge_list)):
        if segments_intersect(edge_list[i][0], edge_list[i][1], edge_list[j][0], edge_list[j][1]):
          valid = False
          # ic(edge_list[i], edge_list[j])
          # valid = True  # デバッグ用
          break
      if not valid:
        break

    if valid:
      ic(len(edge_list))
      ic(edge_list)
      sorter_list = tmp_sorter_list
      break

  # 時間切れの場合、サンプルの解を出力
  if time.time() - start_time > TIME_LIMIT:
    print("時間切れ", file=sys.stderr)
    sample_ans(N, M, K, d_coord_list, s_coord_list, prob_list)
    sys.exit(0)

  ic(sorter_list)

  # グラフの構築
  graph[-1] = sorter_list[0] + N  # 搬入口から最初の分別器へ接続
  
  for i in range(X):
    sorter_node = sorter_list[i] + N
    graph[sorter_node] = []  # 初期化
    
    # 各分別器は出口1と出口2を持つ
    if i < X-1:
      # 出口1: 次の分別器へ
      graph[sorter_node].append(sorter_list[i+1] + N)
      # 出口2: 対応する処理装置へ
      graph[sorter_node].append(i)
    else:
      # 最後の分別器の場合
      # 出口1: 対応する処理装置へ
      graph[sorter_node].append(i)
      # 出口2: 最後の処理装置へ (余った処理装置)
      if i + 1 < N:
        graph[sorter_node].append(i + 1)
      else:
        # 処理装置が足りない場合は同じ処理装置に両方向かせる
        graph[sorter_node].append(i)

  # ic(graph)

  # sorter_id_listの中身を埋める
  for i in range(X):
    sorter_id_list[sorter_list[i]] = best_sorters[i]

  # 得点の計算
  score = calc_score(N, M, K, graph, prob_list, sorter_id_list, processor_list)

  if MyPC:
    print(f"Score: {score}", file=sys.stderr)

  # ic(sorter_id_list)

  # 出力
  print(*processor_list)
  print(graph[-1])  # 搬入口の接続先分別器
  for i in range(M):
    if sorter_id_list[i] == -1:
      print(-1)
    else:
      print(sorter_id_list[i], graph[i + N][0], graph[i + N][1])  # 分別器の接続先処理装置

if __name__ == "__main__":
  main()