import os
from typing import Tuple, List
import random

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

INLET = (0, 5000)  # 搬入口の座標

random.seed(1317)

def sign(x: int) -> int:
  return 1 if x > 0 else -1 if x < 0 else 0

def orientation(a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int]) -> int:
  cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
  return sign(cross)

# 2つの線分が交差しているかを判定する関数
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
  return (o1 * o2 <= 0) and (o3 * o4 <= 0)

# 条件を満たし、かつ処理装置N個全が接続されているグラフを作成する関数
def make_graph(N: int, M: int, d_coord_list: List[Tuple[int, int]], s_coord_list: List[Tuple[int, int]]) -> List[List[int]]:
  # graph: devices 0..N-1, sorters N..N+M-1, inlet N+M
  graph = [[] for _ in range(N + M + 1)]
  
  # 座標のマッピング: インデックス -> 座標
  coords = {}
  for i in range(N):
    coords[i] = d_coord_list[i]  # 処理装置
  for i in range(M):
    coords[N + i] = s_coord_list[i]  # 分別器
  coords[N + M] = INLET  # 搬入口
  
  # 既存の接続を記録（線分交差チェック用）
  existing_connections = []
  
  def can_connect(from_node: int, to_node: int) -> bool:
    """2つのノードを接続できるかチェック"""
    if from_node == to_node:
      return False
    
    # 新しい線分
    new_segment = (coords[from_node], coords[to_node])
    
    # 既存の線分との交差チェック
    for existing_segment in existing_connections:
      if segments_intersect(new_segment[0], new_segment[1], 
                          existing_segment[0], existing_segment[1]):
        return False
    
    return True
  
  def add_connection(from_node: int, to_node: int):
    """接続を追加"""
    graph[from_node].append(to_node)
    existing_connections.append((coords[from_node], coords[to_node]))
  
  # 搬入口に最も近い分別器を見つけて接続
  inlet_node = N + M
  min_dist = float('inf')
  best_sorter = -1
  
  for i in range(M):
    sorter_node = N + i
    if can_connect(inlet_node, sorter_node):
      dist = ((coords[inlet_node][0] - coords[sorter_node][0]) ** 2 + 
              (coords[inlet_node][1] - coords[sorter_node][1]) ** 2) ** 0.5
      if dist < min_dist:
        min_dist = dist
        best_sorter = i
  
  if best_sorter != -1:
    add_connection(inlet_node, N + best_sorter)
  
  # 分別器から処理装置への接続を試行
  # 各分別器について、最も近い2つの処理装置に接続を試行
  for i in range(M):
    sorter_node = N + i
    
    # 処理装置との距離を計算してソート
    device_distances = []
    for j in range(N):
      device_node = j
      if can_connect(sorter_node, device_node):
        dist = ((coords[sorter_node][0] - coords[device_node][0]) ** 2 + 
                (coords[sorter_node][1] - coords[device_node][1]) ** 2) ** 0.5
        device_distances.append((dist, device_node))
    
    device_distances.sort()
    
    # 最大2つの出力先に接続
    connections_made = 0
    for dist, device_node in device_distances:
      if connections_made >= 2:
        break
      if can_connect(sorter_node, device_node):
        add_connection(sorter_node, device_node)
        connections_made += 1
    
    # もし2つの接続ができなかった場合、同じ処理装置に2回接続
    if connections_made == 1 and device_distances:
      # 最初に接続した処理装置に再度接続
      first_device = graph[sorter_node][0]
      graph[sorter_node].append(first_device)
    elif connections_made == 0 and device_distances:
      # 接続できる処理装置があれば、2回接続
      _, best_device = device_distances[0]
      if can_connect(sorter_node, best_device):
        add_connection(sorter_node, best_device)
        graph[sorter_node].append(best_device)
  
  # 分別器間の接続を試行（より複雑なネットワーク構築）
  for i in range(M):
    sorter_i = N + i
    if len(graph[sorter_i]) < 2:  # まだ出力先が足りない分別器
      for j in range(M):
        if i == j:
          continue
        sorter_j = N + j
        
        # 閉路チェック（簡易版）
        if sorter_j in graph[sorter_i] or sorter_i in graph[sorter_j]:
          continue
        
        if can_connect(sorter_i, sorter_j) and len(graph[sorter_i]) < 2:
          add_connection(sorter_i, sorter_j)
  
  # 残りの分別器の出力先を埋める
  for i in range(M):
    sorter_node = N + i
    while len(graph[sorter_node]) < 2:
      # 最も近い処理装置に接続
      min_dist = float('inf')
      best_device = -1
      for j in range(N):
        dist = ((coords[sorter_node][0] - coords[j][0]) ** 2 + 
                (coords[sorter_node][1] - coords[j][1]) ** 2) ** 0.5
        if dist < min_dist:
          min_dist = dist
          best_device = j
      
      if best_device != -1:
        graph[sorter_node].append(best_device)
  
  return graph

def main():
  N, M, K = map(int, input().split())
  d_coord_list = [tuple(map(int, input().split())) for _ in range(N)]  # 処理装置予定地の座標
  s_coord_list = [tuple(map(int, input().split())) for _ in range(M)]  # 分別器の予定地の座標
  
  # 分別確率を読み取る
  p_matrix = []
  for _ in range(K):
    p_matrix.append(list(map(float, input().split())))

  processor_id_list = list(range(N))  # 処理装置は順番通りに配置
  sorter_id_list = [random.randint(0, K-1) for _ in range(M)]  # 分別器はランダムに配置

  graph = make_graph(N, M, d_coord_list, s_coord_list)  # グラフの構築

  # 出力
  print(*processor_id_list)
  print(graph[-1][0])  # 搬入口の接続先分別器
  
  for i in range(M):
    # 使われる分別器
    if len(graph[N + i]) == 2:
      print(sorter_id_list[i], graph[N + i][0], graph[N + i][1])
    else:
      # 分別器が使われない場合は-1を出力
      print(-1)

if __name__ == "__main__":
  main()