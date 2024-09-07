import os
import numpy as np
from scipy.sparse.csgraph import floyd_warshall

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
    adj_list[u-1][v-1] = min(adj_list[u-1][v-1], t) if adj_list[u-1][v-1] != 0 else t
    adj_list[v-1][u-1] = min(adj_list[v-1][u-1], t) if adj_list[v-1][u-1] != 0 else t

  ic(adj_list)

  adj_list = np.array(adj_list)

  # ワーシャルフロイド法で最短経路を求める
  dist_list, pred_list = floyd_warshall(adj_list, return_predecessors=True)

  path_list = [[[] for _ in range(n)] for _ in range(n)]  # 各頂点間の最短経路 ([start][goal])

  # 各頂点間の最短経路を求める
  for start in range(n):
    for goal in range(n):
      path = get_path_row(start, goal, pred_list[start])
      path_list[start][goal] = path

  ic(path_list)

  q = int(input())

  for _ in range(q):
    k = int(input())  # 通る橋の数
    b_list = list(map(int, input().split()))  # 通る橋のリスト




if __name__ == "__main__":
  main()