import os
import random
import math

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

random.seed(1317)  # シードを固定

# シグモイド関数 (現在は不要) 
def sigmoid(x, s):
  a = 1/(1*s)  # 定数。sが大きいほどsigmoid関数の傾きが緩やかになる
  ic(x, 1 / (1 + math.exp(-x*a)))
  return 1 / (1 + math.exp(-x*a))

# 正規分布の乱数を生成
def normal_random(rectangle, s):
  # 確変の長さに対して正規分布の絶対値を足す
  w = rectangle[0] + (random.normalvariate(0, s))
  if w < 1:
    w = 1
  elif 10**9 < w:
    w = 10**9
  h = rectangle[1] + (random.normalvariate(0, s))
  if h < 1:
    h = 1
  elif 10**9 < h:
    h = 10**9
  return w, h

# 長方形を追加した状態のbox_listを作成
def add_rectangle(box_list, ans_list, rectangle, s):
  w, h = normal_random(rectangle, s)
  r, d, b = ans_list[1], 0 if ans_list[2] == "U" else 1, ans_list[3]
  # 回転を行う
  if r:
    w, h = h, w
  # U方向に移動する場合
  if d == 0:
    # 長方形の左端の座標を求める
    if b == -1:
      L = 0
    else:
      L = box_list[d][b][2]
    # 長方形の右端の座標を求める
    R = L + w
    # 長方形が最初に衝突する辺を求める
    for i in range(len(box_list[d])):
      if L < box_list[d][i][2] and box_list[d][i][1] < R:  # 長方形が辺に衝突する場合
        y = box_list[d][i][0]
        break
    # 長方形の座標を追加する
    box_list[d].append([y+h, L, R])
    # box_list[d]をyでソートする
    box_list[d].sort(key = lambda x: x[0], reverse = True)
    # Lの移動に対向する辺を追加する
    box_list[1-d].append([R, y, y+h])
    # box_list[1-d]をRでソートする
    box_list[1-d].sort(key = lambda x: x[0], reverse = True)

  # L方向に移動する場合
  else:
    # 長方形の上端の座標を求める
    if b == -1:
      T = 0
    else:
      T = box_list[d][b][2]
    # 長方形の下端の座標を求める
    B = T + h
    # 長方形が最初に衝突する辺を求める
    for i in range(len(box_list[d])):
      if T < box_list[d][i][2] and box_list[d][i][1] < B:
        x = box_list[d][i][0]
        break
    # 長方形の座標を追加する
    box_list[d].append([x+w, T, B])
    # box_list[d]をxでソートする
    box_list[d].sort(key = lambda x: x[0], reverse = True)
    # Uの移動に対向する辺を追加する
    box_list[1-d].append([B, x, x+w])
    # box_list[1-d]をBでソートする
    box_list[1-d].sort(key = lambda x: x[0], reverse = True)

  return box_list

# コストを計算
def calc_cost(box_list):
  cost = box_list[0][0][0] + box_list[1][0][0]
  return cost

def main():
  n, t, s = map(int, input().split())  # n: 長方形の個数, : 操作回数, s: 標準偏差
  rectangle_list = [list(map(int, input().split())) for _ in range(n)]  # 長方形の  [0]: 横幅, [1]: 縦幅  (短編・長編は不明)

  box_list = []  # 長方形を敷き詰めるリスト [0: Uの移動に対向する辺, 1: Lの移動に対向する辺][長方形の辺 (移動方向に対する座標でソート)][移動方向に対する座標, 支点の座標, 終点の座標]

  # 最大操作回数まで繰り返す
  for i in range(t):
    # ic(i)
    box_list = [[[0, 0, 10**9]], [[0, 0, 10**9]]]
    ans_list = []

    # 貪欲法を用いて長方形を敷き詰める
    for j in range(n):
      # 総当りで最適な位置を探す
      min_cost = 10**10
      best_box_list = []
      best_tmp_ans_list = []
      # 回転の有無
      for r in range(2):
        # 移動方向  (U: 0, L: 1)
        for d in range(2):
          # 基準となる長方形の番号
          for b in range(-1, j):
            tmp_ans_list = [j, r, "L" if d else "U", b]
            # box_listの複製
            tmp_box_list = [[a[:] for a in b] for b in box_list]  # deepcopy
            # 長方形を追加した状態のbox_listを作成
            tmp_box_list = add_rectangle(tmp_box_list, tmp_ans_list, rectangle_list[j], s)
            # コストを計算
            cost = calc_cost(tmp_box_list)
            # 最小コストを更新
            if cost < min_cost:
              min_cost = cost
              best_box_list = tmp_box_list
              best_tmp_ans_list = tmp_ans_list
              if i == 0:
                ic(min_cost, best_tmp_ans_list)

      # ans_list, box_listを更新
      ans_list.append(best_tmp_ans_list)
      box_list = best_box_list

    # 出力
    print(n)
    print("#", i)  # コメントアウト
    for j in range(n):
      print(*ans_list[j])


if __name__ == "__main__":
  main()