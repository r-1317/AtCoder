import os
import sys
import math

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

##### 十字にバス路線を制定 #####

# ユークリッド距離
def dist(a, b):
  return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


# 目的地とのユークリッド距離が最も近い都市を返す
def next_city(g_list, p_list, pos_from, pos_to, tmp_path_list, ng_set):
  # 隣接リストを距離順にソート
  g_list[pos_from].sort(key=lambda x: dist(p_list[x], p_list[pos_to]))

  # 隣接リストの都市のうち、tmp_path_listに含まれていない都市を返す
  for city in g_list[pos_from]:
    if not(city in tmp_path_list or city in ng_set):
      return city


# 移動経路を求める
def find_path(g_list, p_list, pos_from, pos_to, defalut_ng_set):
  tmp_path_list = [-1] * 600  # 一時的な移動経路リスト
  index = 0  # tmp_path_listのインデックス
  ng_set = defalut_ng_set.copy()  # 通れない都市の集合

  # 目的地に到達するまで移動
  while pos_from != pos_to:
    # 目的地とのユークリッド距離が最も近い都市を取得
    next_pos = next_city(g_list, p_list, pos_from, pos_to, tmp_path_list, ng_set)

    # ic(next_pos)

    # 行ける都市がない場合
    if next_pos is None:
      # 一つ前の都市に戻る  
      index -= 1
      ng_set.add(pos_from)
      pos_from = tmp_path_list[index-1]
      continue

    # tmp_path_listに都市を追加
    tmp_path_list[index] = next_pos
    index += 1
    # 現在地を更新
    pos_from = next_pos

  # ic(pos_from)

  # 移動経路を返す
  return tmp_path_list[:index]


# 最もtargetに近いの都市を求める
def find_nearest(p_list, target):
  min_dist = 10**9
  nearest = 0

  for i, p in enumerate(p_list):
    d = dist(p, target)  # 目標地点とのユークリッド距離
    if d < min_dist:
      min_dist = d
      nearest = i

  return nearest

# 最寄りの駅を求める
def find_nearest_station(g_list, p_list, stations_list, pos, defalut_ng_set):
  min_path = 10**9
  nearest = -1
  d_list = [10**9] * 600

  # すべての駅までのユークリッド距離を求める
  for station in stations_list:
    d_list[station] = dist(p_list[pos], p_list[station])

  # d_listをソートしたリストを作成
  sorted_d_list = sorted(d_list)

  stations_set = set(stations_list)  # 重複を除いた駅の集合

  # 近い駅を最大100個まで求める
  near_list = [-1]*min(100, len(stations_set))
  for i in range(len(near_list)):
    near_list[i] = d_list.index(sorted_d_list[i])

  # 近い駅までの経路を求める
  for station in near_list:
    path = find_path(g_list, p_list, pos, station, defalut_ng_set)
    if len(path) < min_path:
      min_path = len(path)
      nearest = station

  #  # デバッグ用
  #   if pos == 0:
  #     ic(nearest, min_path)

  # # デバッグ用
  # if nearest == 0:
  #   ic(len(stations_list), len(near_list))
  #   ic(stations_list)
  #   ic(pos, near_list)
  #   stations_set = set(stations_list)
  #   ic(len(stations_set), len(stations_list))

  return nearest

# 駅間の経路を求める
def find_station_path(line_list, from_station, to_station):
  # 西,北から東,南に向かっていく場合
  if line_list.index(from_station) < line_list.index(to_station):
    line_type = 0  # 順方向
    station_path = line_list[line_list.index(from_station)+1:line_list.index(to_station)+1]  # 出発駅は含まない
  # 東,南から西,北に向かっていく場合
  else:
    line_type = 1  # 逆方向
    station_path = line_list[line_list.index(to_station):line_list.index(from_station)]  # こちらも、出発駅は含まない
    station_path.reverse()

  return station_path, line_type

# 愚直な解法
def main_01(n, m, t, l_a, l_b, g_list, t_list, p_list):
  # # 入力処理
  # n, m, t, l_a, l_b = map(int, input().split())  # n = 都市の数, m = 道路の数, t = 目的地の数, l_a = 配列Aの長さ, l_b = 配列Bの長さ
  # # n, t は常に600
  # ic(n, m, t, l_a, l_b)

  # g_list = [[] for _ in range(m)]  # 隣接リスト

  # for _ in range(m):
  #   u, v = map(int, input().split())
  #   g_list[u].append(v)
  #   g_list[v].append(u)

  # ic(g_list)

  # t_list = list(map(int, input().split()))  # 目的地のリスト

  # ic(t_list)

  # p_list = [] # 都市の座標リスト

  # for _ in range(n):
  #   x, y = map(int, input().split())
  #   p_list.append((x, y))

  # ic(p_list)

  path_list = []  # 移動経路リスト
  pos_from = 0  # 現在地

  # すべての目的地について処理
  for pos_to in t_list:
    # 移動経路リストをpath_listに追加
    path_list += find_path(g_list, p_list, pos_from, pos_to, set())
    pos_from = pos_to

  ic(path_list)

  # 配列Aを作成
  # 今回は順番を気にしない
  vartex_list = list(set(path_list))  # 通る都市のリスト

  ic(vartex_list)

  a_list = vartex_list + [0] * (l_a - len(vartex_list))  # 配列A

  ic(a_list)

  # 配列Aを出力
  print(*a_list)

  # 配列Bを初期化
  b_list = a_list[:l_b]
  print(f"s {l_b} 0 0")

  # path_listに沿って移動、信号を制御
  for p in path_list:
    if not(p in b_list) or True:  # 一時的にTrue
      p_index = a_list.index(p)
      print(f"s 1 {p_index} 0")

    print(f"m {p}")

  ic(g_list[105])


def main():
  # 入力処理
  n, m, t, l_a, l_b = map(int, input().split())  # n = 都市の数, m = 道路の数, t = 目的地の数, l_a = 配列Aの長さ, l_b = 配列Bの長さ
  # n, t は常に600
  ic(n, m, t, l_a, l_b)

  g_list = [[] for _ in range(m)]  # 隣接リスト

  for _ in range(m):
    u, v = map(int, input().split())
    g_list[u].append(v)
    g_list[v].append(u)

  ic(g_list[425])

  t_list = list(map(int, input().split()))  # 目的地のリスト
  # ic(t_list)

  p_list = [] # 都市の座標リスト

  for _ in range(n):
    x, y = map(int, input().split())
    p_list.append((x, y))
  # ic(p_list)

  # バス路線を制定
  # 最も中心(500,500)に近いの都市を求める
  center_station = find_nearest(p_list, (500, 500))
  ic(center_station)

  east = find_nearest(p_list, (1000, 500))
  ic(east)
  weast = find_nearest(p_list, (0, 500))
  ic(weast)
  north = find_nearest(p_list, (500, 0))
  ic(north)
  south = find_nearest(p_list, (500, 1000))
  ic(south)

  # 東西線を定める
  east_line = find_path(g_list, p_list, center_station, east, set())
  weast_line = find_path(g_list, p_list, center_station, weast, set())
  weast_line.reverse()
  ic(len(east_line))
  ic(len(weast_line))

  東西線 = weast_line + [center_station] + east_line
  # ic(東西線)
  print("# 東西線:" , *東西線)

  # 南北線を定める
  north_line = find_path(g_list, p_list, center_station, north, set())
  south_line = find_path(g_list, p_list, center_station, south, set())
  north_line.reverse()
  ic(len(north_line))
  ic(len(south_line))

  南北線 = north_line + [center_station] + south_line
  # ic(南北線)
  print("# 南北線:" , *南北線)

  # 【※】順番としては、西から東、北から南に向かっていく

  stations_list = 東西線 + 南北線  # 駅のリスト

  ic(len(東西線), len(南北線))

  # 東西線、南北線をa_listに追加
  a_list = 東西線 + 南北線  # 配列A
  # ic(a_list)

  a_set = set(a_list)  # 配列Aの要素の集合
  # ic(a_set)

  # デバッグ用に、555を10個追加
  # a_list += [555]*10

  # 配列Aの余った部分にt_listの要素を追加
  for t in t_list:
    if len(a_list) == l_a:# 入り切らない場合、愚直な解法を実行
      main_01(n, m, t, l_a, l_b, g_list, t_list, p_list)
      sys.exit()  # プログラムを終了
    if not(t in a_set):
      a_list.append(t)
      a_set.add(t)

  # ic(a_list)

  # まだ余った場合、ない都市を追加
  for i in range(600):
    if len(a_list) == l_a:
      break
    if not(i in a_set):
      a_list.append(i)
      a_set.add(i)

  # それでも余った場合、0で埋める
  a_list += [0] * (l_a - len(a_list))

  # 配列Aを出力
  print(*a_list)

  # 配列Aに入り切らなかった都市をng_setの初期値として設定
  defalut_ng_set = set()
  for i in range(600):
    if not(i in a_set):
      defalut_ng_set.add(i)

  ic(defalut_ng_set)  # ほとんどの場合、空集合である

  path_list = []  # 移動経路リスト
  pos_from = 0  # 現在地
  
  ##### すべての目的地について処理 #####
  for pos_to in t_list:
    # 直接、目的地に行く場合
    direct_path = find_path(g_list, p_list, pos_from, pos_to, defalut_ng_set)
    direct_cost = len(direct_path)  # 直接行く場合の信号操作のコスト
    # ic(direct_path)
    # ic(direct_cost)

    # バス路線を経由する場合
    from_station = find_nearest_station(g_list, p_list, stations_list, pos_from, defalut_ng_set)  # 現在地から最も近い駅
    to_station = find_nearest_station(g_list, p_list, stations_list, pos_to, defalut_ng_set)  # 目的地から最も近い駅

    if pos_to == 445:
      ic(pos_from, pos_to)
      ic(from_station, to_station)

    # 駅までの経路
    from_station_path = find_path(g_list, p_list, pos_from, from_station, defalut_ng_set)
    to_pos_to_path = find_path(g_list, p_list, to_station, pos_to, defalut_ng_set)

    if pos_to == 445:
      ic(from_station_path)
      ic(to_pos_to_path)

    # 駅までの経路のコスト
    bus_cost = len(from_station_path) + len(to_pos_to_path)  # バス路線を経由する場合の信号操作のコスト

    if pos_to == 445:
      ic(bus_cost)

    # 東西線、南北線の駅間の経路を4つに分けて考える

    #line_typeについて
    #1番目の要素は向かう都市、2番目の要素はバスの種類。
    # 0: バスを使わない, 1: 東西線を順方向に, 2: 東西線を逆方向に, 3: 南北線を順方向に, 4: 南北線を逆方向に
    # ここで順方向とは、東西線の場合は西から東、南北線の場合は北から南に向かっていくことを指す。

    # 1. 両方が東西線に含まれる場合
    if from_station in 東西線 and to_station in 東西線:
      single_line = True
      # 東西線の駅間の経路
      station_path, line_type_1 = find_station_path(東西線, from_station, to_station)
      line_type_1 += 1  # 1: 東西線を順方向に, 2: 東西線を逆方向に

    # 2. 両方が南北線に含まれる場合
    elif from_station in 南北線 and to_station in 南北線:
      single_line = True
      # 南北線の駅間の経路
      station_path, line_type_1 = find_station_path(南北線, from_station, to_station)
      line_type_1 += 3  # 3: 南北線を順方向に, 4: 南北線を逆方向に

    # 3. 東西線の駅から南北線の駅に移動する場合
    elif from_station in 東西線 and to_station in 南北線:
      single_line = False
      # 東西線の駅から中心に向かって移動
      to_center_path, line_type_1 = find_station_path(東西線, from_station, center_station)
      line_type_1 += 1  # 1: 東西線を順方向に, 2: 東西線を逆方向に
      # 中心から南北線の駅に向かって移動
      to_station_path, line_type_2 = find_station_path(南北線, center_station, to_station)
      line_type_2 += 3  # 3: 南北線を順方向に, 4: 南北線を逆方向に

    # 4. 南北線の駅から東西線の駅に移動する場合
    else:
      single_line = False
      # 南北線の駅から中心に向かって移動
      to_center_path, line_type_1 = find_station_path(南北線, from_station, center_station)
      line_type_1 += 3  # 3: 南北線を順方向に, 4: 南北線を逆方向に
      # 中心から東西線の駅に向かって移動
      to_station_path, line_type_2 = find_station_path(東西線, center_station, to_station)
      line_type_2 += 1  # 1: 東西線を順方向に, 2: 東西線を逆方向に

    # ic(single_line)
    # 駅間の経路のコストを計算
    if single_line:
      bus_cost += math.ceil(len(station_path)/l_b)  # バス路線では、l_b個の都市を一度に移動できる
    else:
      bus_cost += math.ceil(len(to_center_path)/l_b) + math.ceil(len(to_station_path)/l_b)
    # ic(bus_cost)

    # コストが小さい方を選択
    # 直接行く場合
    if direct_cost <= bus_cost:
      tmp_path_list = [[city, 0] for city in direct_path]

    # バス路線を経由する場合
    else:
      # 乗る駅までの経路を追加
      tmp_path_list = [[city, 0] for city in from_station_path]

      if single_line:  # 1つの路線のみを使う場合
        tmp_path_list += [[city, line_type_1] for city in station_path]
      else:  # 2つの路線を使う場合
        tmp_path_list += [[city, line_type_1] for city in to_center_path]
        # 中央駅はlype_2にする
        if len(tmp_path_list):  # 既に中央駅に到達している場合は除外
          tmp_path_list[-1][1] = line_type_2
        tmp_path_list += [[city, line_type_2] for city in to_station_path]

      if pos_to == 445:
        ic(tmp_path_list)
      
      # 降りた駅から目的地までの経路を追加
      tmp_path_list += [[city, 0] for city in to_pos_to_path]

    # path_listに追加
    path_list += tmp_path_list

    # デバッグ用
    if pos_to == 445:
      ic(tmp_path_list)
      ic(path_list)

    # 現在地を更新
    pos_from = pos_to

  # 配列Bを初期化
  b_list = [-1]*l_b

  # path_listに沿って移動、信号を制御
  for p, line_type in path_list:
    # 配列Bに含まれていない場合
    if not(p in b_list):
      # バスを用いない場合
      if line_type == 0:
        p_index = a_list.index(p)
        b_list[0] = p
        print(f"s 1 {p_index} 0")
      # 東西線を順方向に使う場合
      elif line_type == 1:
        p_index = 東西線.index(p)
        b_list = a_list[p_index:p_index+l_b]
        print(f"s {l_b} {p_index} 0")
      # 東西線を逆方向に使う場合
      elif line_type == 2:
        p_index = 東西線.index(p)
        if p_index-l_b+1 < 0:  # indexが負になる場合
          b_list = a_list[:l_b]
          print(f"s {l_b} 0 0")
        else:  # indexが正の場合
          b_list = a_list[p_index-l_b+1:p_index+1]
          print(f"s {l_b} {p_index-l_b+1} 0")
      # 南北線を順方向に使う場合
      elif line_type == 3:
        p_index = 南北線.index(p) + len(東西線)  # 東西線の長さを加算
        b_list = a_list[p_index:p_index+l_b]
        print(f"s {l_b} {p_index} 0")
      # 南北線を逆方向に使う場合
      elif line_type == 4:
        p_index = 南北線.index(p) + len(東西線)  # 東西線の長さを加算
        if p_index-l_b+1 < 0:  # indexが負になる場合
          b_list = a_list[:l_b]
          print(f"s {l_b} 0 0")
        else:  # indexが正の場合
          b_list = a_list[p_index-l_b+1:p_index+1]
          print(f"s {l_b} {p_index-l_b+1} 0")

    # 移動
    print(f"m {p}")

  ic.enable() if MyPC else None

  # ic(path_list[:100])


if __name__ == "__main__":
  main()