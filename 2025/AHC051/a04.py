import os
from typing import Tuple
import random
import time
import sys

start_time = time.time()

INLET = (0, 5000)  # 搬入口の座標
MAX_X = 5  # 分別器をつなげる数

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

  # 各ゴミに対して、最も高確率で転送できる分別器を見つける
  best_sorters = [-1] * N
  for i in range(N):
    best_prob = 0
    for j in range(K):
      prob = prob_list[j][i]
      if prob > best_prob:
        best_prob = prob
        best_sorters[i] = j

  ic(best_sorters)

  # 分別器の予定地をランダムにN-1個選び、接続が可能なら採用
  while time.time() - start_time < 1.5:
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

  # 時間切れの場合、01の解を出力
  if time.time() - start_time > 1.7:
    print("時間切れ", file=sys.stderr)
    print(*range(N))
    print(0)
    for _ in range(M):
      print(-1)
    sys.exit(0)

  ic(sorter_list)

  # グラフの構築
  graph[-1] = sorter_list[0] + N  # 搬入口から最初の分別器へ接続
  # for i in range(X-1):
  for i in range(X):
    graph[sorter_list[i] + N].append(i)  # 分別器から処理装置へ接続
    # if i < X-2:
    if i < X-1:
      graph[sorter_list[i] + N].append(sorter_list[i+1] + N)  # 分別器同士を接続
    else:
      graph[sorter_list[i] + N].append(i + 1)  # 最後の分別器から最後の処理装置へ接続

  # ic(graph)

  # sorter_id_listの中身を埋める
  for i in range(X):
    sorter_id_list[sorter_list[i]] = best_sorters[i]

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