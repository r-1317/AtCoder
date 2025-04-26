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
    # if MyPC and i == 0:
      # ic(g_list[i], group_set_list[i])
    print(*group_set_list[i])
    # グループの辺をすべて出力
    for edge in edge_list_list[i]:
      print(*edge)


if __name__ == "__main__":
  main()