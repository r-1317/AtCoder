import os
from typing import Tuple

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

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

# グループを作成する関数
def make_group(g: int, near_city_list: list, city_coord_list: list, is_grouped_list: list) -> list:
  group = []  # グループのリスト
  subgroup_count = 0  # サブグループの数
  city_count = 0  # このグループに属する都市の数。最終的にはg個になる。
  # まずはグループに属していない都市の中で、最も番号が若い都市を選ぶ
  for i in range(N):
    if not is_grouped_list[i]:
      group.append([i])  # グループの最初のサブグループに都市iを追加
      city_count += 1  # 都市iをグループに追加したので、都市の数を1増やす
      is_grouped_list[i] = True  # 都市iはグループに属しているとマーク
      subgroup_count += 1  # サブグループの数を1増やす
      break
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


def main():
  global N, M, Q, L, W
  N, M, Q, L, W = map(int, input().split()) # N: 都市の数, M: 都市をm個のグループに分ける, Q: 占いの上限回数, L: 占いに使う都市の数の上限, W: 都市の座標が含まれる長方形の幅や高さとして有り得る最大値
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

  # 各都市のグループを決定
  # グループCに対して、Cのいずれかの要素との距離が最も近い都市を新たにCに加える
  # グループCは、大きさがL以下のサブグループに分けることができる
  # グループCiの大きさがLを超えるたびに、グループをCi, Ci+1に分割し、CiとCi+1の両方に属する都市cを1つ選ぶ。
  # リストには[..., Ci, Ci+1, Ci+2, ...]と保存する
  group_list = [[] for _ in range(M)]  # グループのリスト

  is_grouped_list = [False] * N  # 都市iがすでにグループに属しているか否か
  
  # 各グループの都市を決定
  for i in range(M):
    group_list[i] = make_group(g_list[i], near_city_list, city_coord_list, is_grouped_list)  # グループを作成

  # グループごとの必要な辺を占いによって取得
  edge_list_list = [[] for _ in range(M)]  # グループごとの必要な辺のリスト

  for i in range(M):
    for subgroup in group_list[i]:
      if len(subgroup) == 1:  # サブグループの都市の数が1の場合、占いは不要
        continue
      # 占いの実行
      print("?", len(subgroup), *subgroup)
      # サブグループの都市の座標を元に、必要な辺を占いによって取得
      tmp_edge_list = [list(map(int, input().split())) for _ in range(len(subgroup) - 1)]
      edge_list_list[i].extend(tmp_edge_list)  # 必要な辺を追加

  # グループごとの都市の集合を作成
  group_set_list = [set() for _ in range(M)]  # グループの都市の集合
  for i in range(M):
    for subgroup in group_list[i]:
      group_set_list[i].update(subgroup)  # サブグループの都市を追加

  # グループごとの必要な辺を出力
  print("!")
  for i in range(M):
    # グループの都市の数と都市の番号を出力
    if MyPC and i == 0:
      ic(g_list[i], group_set_list[i])
    print(*group_set_list[i])
    # グループの辺をすべて出力
    for edge in edge_list_list[i]:
      print(*edge)


if __name__ == "__main__":
  main()