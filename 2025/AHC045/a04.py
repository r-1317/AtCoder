import os
from typing import Tuple
import time

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

start_time = time.time()  # 開始時刻を記録

# グループのいずれかの要素との距離が最も近い都市を探す関数
def nearest_city(group: list, near_city_list: list, is_grouped_list: list) -> Tuple[int, int]:
  min_dist = float("inf")  # 最小距離
  nearest_city = None  # 最も近い都市の番号
  parent_city = None  # 最も近い都市の親都市
  for city in group:
    for i in range(len(near_city_list[city])):
      if is_grouped_list[near_city_list[city][i][0]]:
        continue
      if near_city_list[city][i][1] < min_dist:
        min_dist = near_city_list[city][i][1]
        nearest_city = near_city_list[city][i][0]
        parent_city = city
      break  # 最も近い都市が見つかったら、次に移る
  if nearest_city is None:
    ic(is_grouped_list)
    raise ValueError("No ungrouped city found.")
  return nearest_city, parent_city  # 最も近い都市の番号と親都市の番号を返す

# 原点(0, 0)からの距離が最も遠い都市を探す関数
def find_farthest(city_coord_list: list, is_grouped_list: list) -> int:
  max_dist = -1  # 最大距離
  farthest_city = None  # 原点から最も遠い都市の番号
  # グループに属さない都市の中で、原点からの距離が最も遠い都市を探す
  for i in range(N):  # 都市の数だけループ
    # グループに属している都市はスキップ
    if is_grouped_list[i]:
      continue
    dist = city_coord_list[i][0] ** 2 + city_coord_list[i][1] ** 2  # 原点からの距離の2乗
    # 原点からの距離が最大の場合、都市を更新
    if max_dist < dist:
      max_dist = dist
      farthest_city = i
  # 原点からの距離が最大の都市が見つからなかった場合、エラーを返す
  # これはあり得ないはずだが、念のため
  if farthest_city is None:
    # ic(is_grouped_list)
    raise ValueError("No ungrouped city found.")
  return farthest_city  # 原点から最も遠い都市の番号を返す

# グループを作成する関数
def make_group(g: int, near_city_list: list, city_coord_list: list, is_grouped_list: list) -> list:
  group = []  # グループのリスト
  subgroup_count = 0  # サブグループの数
  city_count = 0  # このグループに属する都市の数。最終的にはg個になる。

  # まずはグループの始点となる都市を選ぶ
  # 原点(0, 0)からの距離が最も遠い都市をグループの始点とする
  first_city = find_farthest(city_coord_list, is_grouped_list)  # 原点から最も遠い都市を選ぶ
  group.append([first_city])  # グループの最初のサブグループに都市iを追加
  city_count += 1  # 都市iをグループに追加したので、都市の数を1増やす
  is_grouped_list[first_city] = True  # 都市iはグループに属しているとマーク
  subgroup_count += 1  # サブグループの数を1増やす

  # グループに都市を追加していく
  while city_count < g:
    # グループのいずれかの要素との距離が最も近い都市を探し、追加する
    new_city, parent_city = nearest_city(group[-1], near_city_list, is_grouped_list)
    # 現在のサブグループの大きさがL未満の場合、都市を追加する
    if len(group[-1]) < L:
      group[-1].append(new_city)  # 都市を追加
      city_count += 1  # 都市の数を1増やす
      is_grouped_list[new_city] = True  # 新しい都市はグループに属しているとマーク
    # 現在のサブグループの大きさがL以上の場合、グループを分割する
    else:
      # グループを分割する
      subgroup_count += 1  # サブグループの数を1増やす
      group.append([parent_city, new_city])  # 新しいサブグループを作成し、都市を追加
      city_count += 1  # 都市の数を1増やす
      is_grouped_list[new_city] = True  # 新しい都市はグループに属しているとマーク
  
  return group  # グループを返す

# すべての辺の長さを計算する関数
def calc_sum_edge_length(edge_list: list, city_coord_list: list) -> float:
  sum_edge_length = 0.0  # すべての辺の長さの合計
  for i in range(M):
    for edge in edge_list[i]:
      # 都市の座標を取得
      x1, y1 = city_coord_list[edge[0]]
      x2, y2 = city_coord_list[edge[1]]
      # 辺の長さを計算
      length = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
      sum_edge_length += length  # 辺の長さを加算

  return sum_edge_length  # すべての辺の長さの合計を返す

# 最も長い辺を探す関数
def find_max_edge(edge_list: list, city_coord_list: list) -> Tuple[int, int]:
  max_edge = None  # 最も長い辺の都市のタプル
  max_edge_length = -1.0  # 最も長い辺の長さ
  for i in range(M):
    for edge in edge_list[i]:
      # 都市の座標を取得
      x1, y1 = city_coord_list[edge[0]]
      x2, y2 = city_coord_list[edge[1]]
      # 辺の長さを計算
      length = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
      # 辺の長さが最大の場合、都市を更新
      if max_edge_length < length:
        max_edge_length = length
        max_edge = edge
  # 辺の長さが最大の都市が見つからなかった場合、エラーを返す
  # これはあり得ないはずだが、念のため
  if max_edge is None:
    # ic(edge_list)
    raise ValueError("No edge found.")

  return max_edge  # 最も長い辺の都市のタプルと長さを返す

# 頂点xとyを入れ替えたグラフを作成する関数
def swap(edge_list: list, x: int, y: int) -> list:
  new_edge_list = [[] for _ in range(M)]  # 新しい辺のリスト
  # 基本的に、元の辺のリストをコピーする
  for i in range(M):
    for edge in edge_list[i]:
      u, v = edge  # 辺の都市の番号
      # 頂点xとyを入れ替える
      if u == x:
        u = y
      elif u == y:
        u = x
      if v == x:
        v = y
      elif v == y:
        v = x
      new_edge_list[i].append((u, v))  # 新しい辺を追加
  # 新しい辺のリストを返す
  return new_edge_list

def main():
  global N, M, Q, L, W  # グローバル変数の宣言
  # 入力の取得
  # N: 都市の数, M: 都市をm個のグループに分ける, Q: 占いの上限回数, L: 占いに使う都市の数の上限, W: 都市の座標が含まれる長方形の幅や高さとして有り得る最大値
  N, M, Q, L, W = map(int, input().split())
  g_list = list(map(int, input().split())) # 各都市グループの都市の数。リストの長さはm

  city_coord_list = [] # 都市の座標リスト
  # 都市の座標を取得
  for i in range(N):
    lx, rx, ly, ry = map(int, input().split())  # 都市が含まれる長方形範囲の端2点の座標
    x = (lx + rx) / 2
    y = (ly + ry) / 2
    city_coord_list.append((x, y))

  # 各都市に対し、距離が近い順にソートした都市のリストを作成
  near_city_list = [[] for _ in range(N)] # 都市iに近い順にソートした都市のリスト
  for i in range(N):
    dist_list = []  # 都市iからの距離の2乗のリスト
    # 都市iからの距離の2乗を計算
    for j in range(N):
      # if i == j:
      #   continue
      dist = (city_coord_list[i][0] - city_coord_list[j][0]) ** 2 + (city_coord_list[i][1] - city_coord_list[j][1]) ** 2  # 距離の2乗
      dist_list.append(dist)
    # 都市iからの距離の2乗に基づいて都市jをソート
    tmp_city_list = []
    # 都市iからの距離の2乗と都市jの番号をタプルにして追加
    for j in range(N):
      if i == j:
        continue
      tmp_city_list.append((j, dist_list[j]))  # 都市iからの距離の2乗と都市jの番号をタプルにして追加
    tmp_city_list.sort(key=lambda x: x[1])  # 都市iからの距離の2乗でソート
    near_city_list[i] = tmp_city_list  # 都市iに近い順にソートした都市のリストを保存

  # g_listを降順にソートしたリストの各要素のインデックスを保存
  sorted_g_list_index_list = sorted(range(M), key=lambda x: g_list[x], reverse=True)
  # ic(sorted_g_list_index_list)

  # 各都市のグループを決定
  # グループCに対して、Cのいずれかの要素との距離が最も近い都市を新たにCに加える
  # グループCは、大きさがL以下のサブグループに分けることができる
  # グループCiの大きさがLを超えるたびに、グループをCi, Ci+1に分割し、CiとCi+1の両方に属する都市cを1つ選ぶ。
  # リストには[..., Ci, Ci+1, Ci+2, ...]と保存する
  group_list = [[] for _ in range(M)]  # グループのリスト

  is_grouped_list = [False] * N  # 都市iがすでにグループに属しているか否か
  
  # 各グループの都市を決定
  for i in sorted_g_list_index_list:  # 降順にソートしたリストの各要素のインデックスを使用
    group_list[i] = make_group(g_list[i], near_city_list, city_coord_list, is_grouped_list)  # グループを作成

  # グループごとの必要な辺を占いによって取得
  edge_list = [[] for _ in range(M)]  # グループごとの必要な辺のリスト

  for i in range(M):
    for subgroup in group_list[i]:
      if len(subgroup) == 1:  # サブグループの都市の数が1の場合、占いは不要
        continue
      # 占いの実行
      print("?", len(subgroup), *subgroup)
      # サブグループの都市の座標を元に、必要な辺を占いによって取得
      tmp_edge_list = [list(map(int, input().split())) for _ in range(len(subgroup) - 1)]
      edge_list[i].extend(tmp_edge_list)  # 必要な辺を追加

  # グループごとの都市の集合を作成
  group_set_list = [set() for _ in range(M)]  # グループの都市の集合
  for i in range(M):
    for subgroup in group_list[i]:
      group_set_list[i].update(subgroup)  # サブグループの都市を追加

  # すべての辺の長さを計算
  sum_edge_length = calc_sum_edge_length(edge_list, city_coord_list)  # すべての辺の長さを計算
  # 最も長い辺を探す
  max_edge = find_max_edge(edge_list, city_coord_list)  # 最も長い辺を探す
  u, v = max_edge  # 最も長い辺の頂点
  best_u, best_v = u, v  # 入れ替える先の都市の番号

  # u, vを別の都市に置き換え、長さの合計が最小になるように山登り
  for x in (u, v):  # 置き換えるもとの都市u, vの順にループ
    for i in range(N):  # 置き換える都市の候補
      if i == u or i == v:  # 置き換える都市と同じ場合、スキップ
        continue
      # xとiを入れ替えたグラフの辺の長さの合計を計算
      tmp_edge_list = swap(edge_list, x, i)  # xとiを入れ替える
      tmp_sum_edge_length = calc_sum_edge_length(tmp_edge_list, city_coord_list)  # すべての辺の長さを計算
      # 辺の長さの合計が小さい場合、xとiを入れ替える
      if tmp_sum_edge_length < sum_edge_length:
        edge_list = tmp_edge_list
        sum_edge_length = tmp_sum_edge_length
        # 都市のグループの集合からもxとiを入れ替える
        for j in range(M):
          if x in group_set_list[j]:
            group_set_list[j].remove(x)
            group_set_list[j].add(-1)  # 一時的に都市iを-1とする
          if i in group_set_list[j]:
            group_set_list[j].remove(i)
            group_set_list[j].add(x)
          if -1 in group_set_list[j]:  # -1がある場合、都市iに置き換える
            group_set_list[j].remove(-1)
            group_set_list[j].add(i)


  # グループごとの必要な辺を出力
  print("!")
  for i in range(M):
    # グループの都市の数と都市の番号を出力
    # if MyPC and i == 0:
      # ic(g_list[i], group_set_list[i])
    print(*group_set_list[i])
    # グループの辺をすべて出力
    for edge in edge_list[i]:
      print(*edge)


if __name__ == "__main__":
  main()