import os

MyPC = os.path.basename(__file__) != "Main.py"
# MyPC = False  # テスト用
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

##### 愚直に実装 #####

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
def find_path(g_list, p_list, pos_from, pos_to):
  tmp_path_list = [-1] * 600  # 一時的な移動経路リスト
  index = 0  # tmp_path_listのインデックス
  ng_set = set()  # 通れない都市の集合

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

    # path_listに都市を追加
    tmp_path_list[index] = next_pos
    index += 1
    # 現在地を更新
    pos_from = next_pos

  ic(pos_from)

  # 移動経路を返す
  return tmp_path_list[:index]

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

  ic(g_list)

  t_list = list(map(int, input().split()))  # 目的地のリスト

  ic(t_list)

  p_list = [] # 都市の座標リスト

  for _ in range(n):
    x, y = map(int, input().split())
    p_list.append((x, y))

  ic(p_list)

  path_list = []  # 移動経路リスト
  pos_from = 0  # 現在地

  # すべての目的地について処理
  for pos_to in t_list:
    # 移動経路リストをpath_listに追加
    path_list += find_path(g_list, p_list, pos_from, pos_to)
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


if __name__ == "__main__":
  main()