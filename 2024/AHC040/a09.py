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

# シグモイド関数
def sigmoid(x, s):
  a = 1/(1*s)  # 定数。sが大きいほどsigmoid関数の傾きが緩やかになる
  ic(x, 1 / (1 + math.exp(-x*a)))
  return 1 / (1 + math.exp(-x*a))

# 正規分布の乱数を生成
def normal_random(rectangle_list, s):
  return_list = []
  for rectangle in rectangle_list:
    # 確変の長さに対して正規分布の絶対値を足す
    w = rectangle[0] + (random.normalvariate(0, s))
    w = int(w)
    if w < 1:
      w = 1
    elif 10**9 < w:
      w = 10**9
    h = rectangle[1] + (random.normalvariate(0, s))
    h = int(h)
    if h < 1:
      h = 1
    elif 10**9 < h:
      h = 10**9
    return_list.append([w, h])
  return return_list

# 長方形を追加した状態のbox_listを作成
def add_rectangle(box_list, ans_list, rectangle, s):
  w, h = rectangle
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
      # ic(len(box_list[d]), b)
      # ic(d, b, box_list[d][b])
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

def main():
  n, t, s = map(int, input().split())  # n: 長方形の個数, : 操作回数, s: 標準偏差
  rectangle_list = [list(map(int, input().split())) for _ in range(n)]  # 長方形の  [0]: 横幅, [1]: 縦幅  (短編・長編は不明)

  start = max(4, int(math.sqrt(n))-3)
  end = min(n//4, int(math.sqrt(n))+5)
  # m = min(t, n)  # 
  # prob = 1/8  # 逆張り回転をする確率

  x_list = [i for i in range(start, end+1)]*100  # 1列の個数を格納した、十分に長いリスト
  # ic(x_list)

  # 最大操作回数まで繰り返す
  for i in range(t):
    tmp_rectangle_list = normal_random(rectangle_list, s)
    # ic(i)
    x = x_list[i]
    box_list = [[[0, 0, 10**9]], [[0, 0, 10**9]]]  # [0]: U方向のbox_list, [1]: L方向のbox_list
    ans_list = []
    # 長方形を敷き詰める
    tmp = -1  # 何番目の長方形まで敷き詰めたか
    while tmp < n-1:
      # 回転の有無をビット全探索
      min_cost = 10**18
      best_ans_list = []
      best_box_list = []
      max_p = min(tmp+x, n-1)  # 一度に敷き詰める長方形の個数
      rect_count = max_p - tmp
      # 回転の有無をビット全探索
      for j in range(2**rect_count):
        tmp_ans_list = [[] for _ in range(rect_count)]
        tmp_box_list = [[a[:] for a in b] for b in box_list] # box_listのコピー
        # tmp_ans_listを作成
        for k in range(rect_count):
          tmp_ans_list[k] = [tmp+k+1, 0, "U", tmp+k]
          # xの倍数の場合はリセット
          if (tmp+k+1)%x == 0:
            tmp_ans_list[k][3] = -1
          # 回転の有無を決定
          tmp_ans_list[k][1] = (j >> k) & 1
          # tmp_box_listに長方形を追加
          tmp_box_list = add_rectangle(tmp_box_list, tmp_ans_list[k], tmp_rectangle_list[tmp+k+1], s)
        # コストを計算
        cost = tmp_box_list[0][0][0] + tmp_box_list[1][0][0]
        # 最小コストを更新
        if cost < min_cost:
          min_cost = cost
          best_ans_list = tmp_ans_list
          best_box_list = tmp_box_list
      # 敷き詰めた長方形の個数を更新
      tmp += rect_count
      # ans_listに追加
      for j in range(rect_count):
        ans_list.append(best_ans_list[j])
      # box_listを更新
      box_list = best_box_list
    # 出力
    print(n)
    print("#", x)  # コメントアウト
    for j in range(n):
      print(*ans_list[j])

if __name__ == "__main__":
  main()