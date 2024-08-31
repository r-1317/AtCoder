import os
import numpy as np
from scipy.sparse.csgraph import dijkstra

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# 直前の頂点を辿ることで最短経路を求める
def get_path_row(start, goal, pred_row):
  path = [-1] * 600
  index = 0
  i = goal
  while i != start and i >= 0:
    path[index] = i
    i = pred_row[i]
    index += 1
  if i < 0:
    return None
  path.append(i)
  path = path[:index]
  return path[::-1]

def main():
  n, m = map(int, input().split())  # n: 島の数, m: 橋の数
  edge_list = [list(map(int, input().split())) for _ in range(m)]  # 橋のリスト

  adj_list = [[0]*n for _ in range(n)]  # 隣接行列

  for edge in edge_list:
    u, v, t = edge  # u: 始点, v: 終点, t: 時間
    adj_list[u-1][v-1] = min(adj_list[u-1][v-1], t)
    adj_list[v-1][u-1] = min(adj_list[v-1][u-1], t)

  ic(adj_list)

  adj_list = np.array(adj_list)

  # ダイクストラ法で最短経路を求める
  dist_list, pred_list = dijkstra(adj_list, indices=0, directed=False, return_predecessors=True)
  defalut_dist = dist_list[n-1]  # 0からn-1までの最短経路

  path = get_path_row(0, n-1, pred_list)  # 0からn-1までの最短経路
  ic(path)

  loss_list = [0]*n  # 時間ロスのリスト

  for i, edge in enumerate(edge_list):
    u, v, t = edge
    loss = t - adj_list[u-1][v-1]
    loss_list[i] = loss

  ic(loss_list)

  q = int(input())  # クエリの数

  for _ in range(q):
    k = int(input())




if __name__ == "__main__":
  main()