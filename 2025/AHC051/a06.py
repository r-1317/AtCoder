import os
from typing import Tuple, List
import random
import time
import sys
import math
import itertools

start_time = time.time()

INLET = (0, 5000)  # 搬入口の座標
X06 = 3  # 分別器の数(2^n - 1 を満たす必要がある)
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

# 搬入口に近い分別器max_count個を探す関数
def find_nearest_sorter(s_coord_list: List[Tuple[int, int]], max_count: int) -> List[int]:
  inlet = INLET
  # (距離の二乗, インデックス) のリストを作成
  dist_with_idx = []
  for idx, (x, y) in enumerate(s_coord_list):
    dx = x - inlet[0]
    dy = y - inlet[1]
    dist_sq = dx * dx + dy * dy
    dist_with_idx.append((dist_sq, idx))
  # 距離でソートして上位 max_count 件のインデックスを返す
  dist_with_idx.sort(key=lambda t: t[0])
  return [idx for _, idx in dist_with_idx[:max_count]]

def main():
  N, M, K = map(int, input().split())  # N: ゴミの種類の数であり処理装置の数, M: 分別器の数, K: 分別器の種類の数
  d_coord_list = [tuple(map(int, input().split())) for _ in range(N)]  # 処理装置予定地の座標
  s_coord_list = [tuple(map(int, input().split())) for _ in range(M)]  # 分別器の予定地の座標

  prob_list = [list(map(float, input().split())) for _ in range(K)]  # 各分別器のゴミiの転送確率

  processor_id_list = list(range(N))
  sorter_id_list = [-1] * M
  processor_list = list(range(N))  # 処理装置は順番通りに配置

  graph = [[] for _ in range(N+M+1)]  # [処理装置(N個), 分別器(M個), 搬入口(1個)]の順

  # スコアが最も小さくなる分別器の組み合わせ
  best_sorters = [-1] * N

  ic(len(s_coord_list))

  nearest_sorter_5 = find_nearest_sorter(s_coord_list, 5)

  ic(nearest_sorter_5)
  for i in range(len(nearest_sorter_5)):
    ic(s_coord_list[nearest_sorter_5[i]])

    ############# ここまでやった #############

  # 分別器をnearest_sorter_5から3つの順列組み合わせを選ぶ
  for tmp_sorter_list in itertools.permutations(nearest_sorter_5, X06):
    for tmp_processor_list in itertools.permutations(range(X06+1), X06+1):
      edge_list = []
      edge_list.append((INLET, s_coord_list[tmp_sorter_list[0]]))
      edge_list.append((s_coord_list[tmp_sorter_list[0]], s_coord_list[tmp_sorter_list[1]]))
      edge_list.append((s_coord_list[tmp_sorter_list[0]], s_coord_list[tmp_sorter_list[2]]))
      edge_list.append((s_coord_list[tmp_sorter_list[1]], d_coord_list[tmp_processor_list[0]]))
      edge_list.append((s_coord_list[tmp_sorter_list[1]], d_coord_list[tmp_processor_list[1]]))
      edge_list.append((s_coord_list[tmp_sorter_list[2]], d_coord_list[tmp_processor_list[2]]))
      edge_list.append((s_coord_list[tmp_sorter_list[2]], d_coord_list[tmp_processor_list[3]]))

      valid = True

      # 辺が重ならないか
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
        break
    if valid:
      break

  # 最適な分別器の種類を探索
  max_prob = 0.0
  best_sorters = [-1] * X06
  for sorter_0 in range(K):
    for sorter_1 in range(K):
      for sorter_2 in range(K):
        # 処理装置ごとに、適切に処理される確率を求める
        prob = 0
        processor_idx = tmp_processor_list[0]
        prob += 0.25 * prob_list[sorter_0][processor_idx] * prob_list[sorter_1][processor_idx]
        processor_idx = tmp_processor_list[1]
        prob += 0.25 * prob_list[sorter_0][processor_idx] * (1 - prob_list[sorter_1][processor_idx])
        processor_idx = tmp_processor_list[2]
        prob += 0.25 * (1 - prob_list[sorter_0][processor_idx]) * prob_list[sorter_2][processor_idx]
        processor_idx = tmp_processor_list[3]
        prob += 0.25 * (1 - prob_list[sorter_0][processor_idx]) * (1 - prob_list[sorter_2][processor_idx])
        if prob > max_prob:
          max_prob = prob
          best_sorters[0] = sorter_0
          best_sorters[1] = sorter_1
          best_sorters[2] = sorter_2

  # sorter_id_listの初期化
  sorter_id_list = [-1]*M
  for i, s in enumerate(tmp_sorter_list):
    sorter_id_list[s] = best_sorters[i]

  # グラフ構築
  graph[-1] = tmp_sorter_list[0] + N  # 搬入口から最初の分別器へ接続
  graph[tmp_sorter_list[0] + N] = []  # 初期化
  graph[tmp_sorter_list[0] + N].append(tmp_sorter_list[1] + N)
  graph[tmp_sorter_list[0] + N].append(tmp_sorter_list[2] + N)
  graph[tmp_sorter_list[1] + N] = []  # 初期化
  graph[tmp_sorter_list[1] + N].append(tmp_processor_list[0])
  graph[tmp_sorter_list[1] + N].append(tmp_processor_list[1])
  graph[tmp_sorter_list[2] + N] = []  # 初期化
  graph[tmp_sorter_list[2] + N].append(tmp_processor_list[2])
  graph[tmp_sorter_list[2] + N].append(tmp_processor_list[3])

  # 時間切れの場合、サンプルの解を出力
  if time.time() - start_time > TIME_LIMIT:
    print("時間切れ", file=sys.stderr)
    sample_ans(N, M, K, d_coord_list, s_coord_list, prob_list)
    sys.exit(0)

  # ic(sorter_list)

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