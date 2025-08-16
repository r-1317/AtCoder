import os
from typing import Tuple, List
import random
import time
import sys
import math
import itertools

start_time = time.time()

INLET = (0, 5000)  # 搬入口の座標
TIME_LIMIT = 1.8  # 秒
X07 = 4  # 完全二分木の高さ

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

# スコア計算関数
def calc_score(N: int, M: int, K: int, graph: list, prob_matrix: list, sorter_id_list: list, processor_list: list) -> float:
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
          p1 = prob_matrix[sorter_type][waste_type]
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

# 分別器を高さ5の完全二分木になるようにつなげ、その末端に2つずつ処理装置を接続する。処理装置は重複してもよい。
def make_binary_tree(N: int, M: int, d_coord_list: List[Tuple[int, int]], s_coord_list: List[Tuple[int, int]]) -> List[List[int]]:
  """高さ X07 の完全二分木 (ソーター 2^X07 -1, 葉 2^{X07-1}) を構築し葉を処理装置へ接続する."""
  graph = [[] for _ in range(N + M + 1)]

  HEIGHT = X07  # レベル数 (root depth=0, leaves depth=HEIGHT-1)
  if HEIGHT < 1:
    return graph
  REQUIRED_SORTERS = (1 << HEIGHT) - 1
  LEAF_COUNT = 1 << (HEIGHT - 1)
  if M < REQUIRED_SORTERS:
    # フォールバック (高さ5 が構築できないケース)
    if M == 0 or N == 0:
      return graph
    root = 0
    graph[N + M] = N + root
    graph[N + root] = [0, 0 if N == 1 else 1 % N]
    return graph

  # 交差判定 (inclusive) 端点共有は許容
  def intersect(a1, a2, b1, b2) -> bool:
    if a1 == b1 or a1 == b2 or a2 == b1 or a2 == b2:
      return False
    if (max(a1[0], a2[0]) < min(b1[0], b2[0]) or
        max(b1[0], b2[0]) < min(a1[0], a2[0]) or
        max(a1[1], a2[1]) < min(b1[1], b2[1]) or
        max(b1[1], b2[1]) < min(a1[1], a2[1])):
      return False
    o1 = orientation(a1, a2, b1)
    o2 = orientation(a1, a2, b2)
    o3 = orientation(b1, b2, a1)
    o4 = orientation(b1, b2, a2)
    return (o1 * o2 <= 0) and (o3 * o4 <= 0)

  edges: List[Tuple[int, int]] = []  # (u_node, v_node)

  def coord(node_id: int) -> Tuple[int, int]:
    if node_id == N + M:
      return INLET
    if node_id < N:
      return d_coord_list[node_id]
    return s_coord_list[node_id - N]

  def edge_crosses(u: int, v: int) -> bool:
    cu, cv = coord(u), coord(v)
    for a, b in edges:
      if not (u == a or u == b or v == a or v == b):
        if intersect(cu, cv, coord(a), coord(b)):
          return True
    return False

  # ソーター候補を距離順に並べ root を決定
  idxs = list(range(M))
  idxs.sort(key=lambda i: (s_coord_list[i][0]-INLET[0])**2 + (s_coord_list[i][1]-INLET[1])**2)
  # root 試行 (複数試して最初に成功したものを採用)
  root_candidates = idxs[:8]

  BEST = None

  # 再帰で31個選んで完全二分木 (配列順) を埋める
  INTERNAL = REQUIRED_SORTERS - LEAF_COUNT  # 内部ノード数 = 2^{H-1}-1

  LIMIT_PAIR_TRY = 40

  def build_with_root(root_sorter_idx: int) -> bool:
    tree_order: List[int] = [None]*REQUIRED_SORTERS  # ソーター index (s_coord_list 内)
    used = set()
    tree_order[0] = root_sorter_idx
    used.add(root_sorter_idx)
    # inlet -> root edge
    edges.clear()
    edges.append((N+M, N+root_sorter_idx))

    # 再帰
    def dfs(i: int) -> bool:
      if i >= INTERNAL:
        return True
      parent_sorter_idx = tree_order[i]
      parent_node = N + parent_sorter_idx
      pc = s_coord_list[parent_sorter_idx]
      # 候補集合 (未使用) 距離 + 角度でソート
      cand = [j for j in idxs if j not in used]
      cand.sort(key=lambda j: (s_coord_list[j][0]-pc[0])**2 + (s_coord_list[j][1]-pc[1])**2)
      # 上側/下側に分けてバランスを取る
      upper = [j for j in cand if s_coord_list[j][1] <= pc[1]]
      lower = [j for j in cand if s_coord_list[j][1] > pc[1]]
      ordered = []
      # 交互に詰める
      while upper or lower:
        if upper:
          ordered.append(upper.pop(0))
        if lower:
          ordered.append(lower.pop(0))
      cand = ordered
      tries = 0
      L = len(cand)
      for a_idx in range(min(L, LIMIT_PAIR_TRY)):
        for b_idx in range(a_idx+1, min(L, a_idx+1+LIMIT_PAIR_TRY)):
          a = cand[a_idx]; b = cand[b_idx]
          node_a = N + a; node_b = N + b
          # 交差検査
          if edge_crosses(parent_node, node_a):
            continue
          # 一時追加して b 判定
          edges.append((parent_node, node_a))
          cross_b = edge_crosses(parent_node, node_b)
          if cross_b:
            edges.pop()
            continue
          edges.append((parent_node, node_b))
          # OK -> 子を登録
            # (注: parent->a, parent->b の間は端点共有なので交差扱いしない)
          c1_pos = 2*i+1; c2_pos = 2*i+2
          tree_order[c1_pos] = a
          tree_order[c2_pos] = b
          used.add(a); used.add(b)
          if dfs(i+1):
            return True
          # backtrack
          used.remove(a); used.remove(b)
          tree_order[c1_pos] = None; tree_order[c2_pos] = None
          edges.pop(); edges.pop()  # parent->b, parent->a
          tries += 1
          if tries > LIMIT_PAIR_TRY:
            break
        if tries > LIMIT_PAIR_TRY:
          break
      return False

    ok = dfs(0)
    if not ok:
      edges.clear()
      return False
    # グラフへ書き込み (内部ノード)
    graph[N+M] = N + tree_order[0]
    for i2 in range(INTERNAL):
      left = tree_order[2*i2+1]
      right = tree_order[2*i2+2]
      graph[N + tree_order[i2]] = [N + left, N + right]
    # 葉 (index INTERNAL .. end) について: 全ての leaf->processor 辺を非交差で2本ずつバックトラック構築
    leaf_indices = tree_order[INTERNAL:]
    # 並べ方: x座標昇順 (左から順) で処理 (交差リスク低減)
    leaf_indices.sort(key=lambda si: s_coord_list[si][0])
    # 候補 processor を距離昇順で事前計算
    proc_candidates: List[List[int]] = []
    for si in leaf_indices:
      sc = s_coord_list[si]
      proc_list_sorted = list(range(N))
      proc_list_sorted.sort(key=lambda p: (d_coord_list[p][0]-sc[0])**2 + (d_coord_list[p][1]-sc[1])**2)
      proc_candidates.append(proc_list_sorted)

    chosen_pairs: List[Tuple[int,int]] = [None]*len(leaf_indices)  # (p1,p2)

    def add_edge(u: int, v: int):
      edges.append((u, v))

    def remove_last_edge():
      edges.pop()

    def dfs_leaf(idx_leaf: int) -> bool:
      if idx_leaf == len(leaf_indices):
        return True
      sorter_idx = leaf_indices[idx_leaf]
      leaf_node = N + sorter_idx
      cands = proc_candidates[idx_leaf]
      # 1本目候補ループ
      for i1, p1 in enumerate(cands):
        if edge_crosses(leaf_node, p1):
          continue
        add_edge(leaf_node, p1)
        # 2本目候補 (異なるもの優先)
        order_second = [p for j,p in enumerate(cands) if j != i1] + [p1]
        for p2 in order_second:
          if edge_crosses(leaf_node, p2):
            continue
          add_edge(leaf_node, p2)
            # 再帰
          chosen_pairs[idx_leaf] = (p1, p2)
          if dfs_leaf(idx_leaf+1):
            return True
          remove_last_edge()  # p2
        remove_last_edge()  # p1
      return False

    if not dfs_leaf(0):
      # 失敗した場合は安全策: 既存 leaf edges を削除して False
      # (root 変更探索に戻る)
      # sorter間エッジ数 = 1 (inlet-root) + 2*(INTERNAL) = 1 + 30 =31
      while len(edges) > 1 + 2*INTERNAL:
        edges.pop()
      return False

    # 成功: graph へ格納
    for idx_leaf, sorter_idx in enumerate(leaf_indices):
      p1, p2 = chosen_pairs[idx_leaf]
      graph[N + sorter_idx] = [p1, p2]
    return True

  for r in root_candidates:
    if build_with_root(r):
      BEST = True
      break

  if BEST is None:
    # どの root でも失敗: 旧フォールバック
    if M == 0 or N == 0:
      return graph
    graph[N+M] = N
    graph[N] = [0, 0 if N == 1 else 1 % N]
  return graph

def main():
  N, M, K = map(int, input().split())  # N: ゴミの種類の数であり処理装置の数, M: 分別器の数, K: 分別器の種類の数
  d_coord_list = [tuple(map(int, input().split())) for _ in range(N)]  # 処理装置予定地の座標
  s_coord_list = [tuple(map(int, input().split())) for _ in range(M)]  # 分別器の予定地の座標

  prob_matrix = [list(map(float, input().split())) for _ in range(K)]  # 各分別器のゴミiの転送確率

  processor_id_list = list(range(N))
  sorter_id_list = [random.randint(0, K-1) for _ in range(M)]  # 分別器の種類IDをランダムに設定
  processor_list = list(range(N))  # 処理装置は順番通りに配置

  graph = [[] for _ in range(N+M+1)]  # [処理装置(N個), 分別器(M個), 搬入口(1個)]の順

  graph = make_binary_tree(N, M, d_coord_list, s_coord_list)  # グラフの構築

  # 得点の計算
  score = calc_score(N, M, K, graph, prob_matrix, sorter_id_list, processor_list)
  ic(score)

  # sorter_id_listの焼きなまし
  temperature = 1.0
  cooling_rate = 0.99
  while time.time() - start_time < TIME_LIMIT:
    # 焼きなましの実行
    new_sorter_id_list = sorter_id_list[:]
    for i in range(M):
      if random.random() < temperature:
        new_sorter_id_list[i] = random.randint(0, K-1)
    new_graph = make_binary_tree(N, M, d_coord_list, s_coord_list)
    new_score = calc_score(N, M, K, new_graph, prob_matrix, new_sorter_id_list, processor_list)
    if new_score < score:
      sorter_id_list = new_sorter_id_list
      graph = new_graph
      score = new_score
    temperature *= cooling_rate

  score = calc_score(N, M, K, graph, prob_matrix, sorter_id_list, processor_list)
  if MyPC:
    print(f"Score: {score}", file=sys.stderr)

  # 出力
  print(*processor_list)
  print(graph[-1])  # 搬入口の接続先分別器
  for i in range(M):
    if len(graph[i + N]) < 2:  # 分別器の出口が足りない場合(=その分別器を使用しない場合)
      print(-1)
    else:
      print(sorter_id_list[i], graph[i + N][0], graph[i + N][1])  # 分別器の接続先処理装置

if __name__ == "__main__":
  main()