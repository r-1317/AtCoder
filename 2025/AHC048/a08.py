import os
from typing import Tuple, List
import math
import random

debug  = True
debug = False
MyPC = os.path.basename(__file__) != "Main.py" and debug
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

N = 20  # 固定
random.seed(1317)  # 再現性のために乱数シードを固定

ic.enable() if MyPC else None

# 指定された位置(x, y)に、指定されたインデックスの絵の具を1グラム追加するコマンドを返す。
def add_paint(well_index: int, paint_index: int) -> List[str]:
  x = well_index // (N // well_size) * well_size
  y = well_index % (N // well_size) * well_size
  return [f"1 {x} {y} {paint_index}"]

# 指定された位置(x, y)の絵の具を提出するコマンドを返す。
def extract_color(well_index: int) -> List[str]:
  x = well_index // (N // well_size) * well_size
  y = well_index % (N // well_size) * well_size
  return [f"2 {x} {y}"]

# 指定された位置(x, y)の絵の具を1グラム破棄するコマンドを返す。
def discard_paint(well_index: int) -> List[str]:
  x = well_index // (N // well_size) * well_size
  y = well_index % (N // well_size) * well_size
  return [f"3 {x} {y}"]

# CMY値の差を計算する関数
def calc_diff(owm: list, target: list) -> float:
  return math.sqrt((target[0] - owm[0]) ** 2 + (target[1] - owm[1]) ** 2 + (target[2] - owm[2]) ** 2)

# 目標色に最も近い色を見つける関数
# def find_nearest_color(palette: List[List[int | float]], target: List[float]) -> Tuple[int, float]:
def find_nearest_color(palette: List[List], target: List[float]) -> Tuple[int, float]:
  nearest_index = -1
  min_diff = 10**9
  for i, paint in enumerate(palette):
    # 絵の具が足りない場合はスキップ
    if paint[0] < 1:
      continue

    cmy = paint[1:4]  # CMY値
    diff = calc_diff(cmy, target)
    if diff < min_diff:
      min_diff = diff
      nearest_index = i

  return nearest_index, min_diff

# def add_to_palette(palette: List[List[int | float]], well_index: int, owm: List[float], amount: int) -> int:
def add_to_palette(palette: List[List], well_index: int, owm: List[float], amount: int) -> int:
  if amount == 0:
    return 0  # 追加する量が0なら何もしない
  # ic(amount)
  # ウェルの現在の絵の具の量を取得
  # ウェルの容量を超えるなら、その分だけ減らす
  discard_count = 0
  # ic(palette[well_index][0])
  for _ in range(amount):
    if well_size**2 < palette[well_index][0] + amount:
      palette[well_index][0] -= 1
      discard_count += 1
  # ic(palette[well_index][0], discard_count)
  
  # ウェルに絵の具を追加
  prev_amount = palette[well_index][0]
  prev_cmy = palette[well_index][1:4]  # CMY値の前の値
  new_amount = prev_amount + amount
  if new_amount > well_size**2:
    # ic(f"ウェルの容量を超えています: {new_amount} > {well_size**2}, discard_count: {discard_count}")
    # ic(new_amount, well_size**2, discard_count)
    raise ValueError("ウェルの容量を超えています")
  new_cmy = [
    (prev_cmy[0] * prev_amount + owm[0] * amount) / new_amount,
    (prev_cmy[1] * prev_amount + owm[1] * amount) / new_amount,
    (prev_cmy[2] * prev_amount + owm[2] * amount) / new_amount
  ]

  # パレットに更新
  palette[well_index] = [new_amount] + new_cmy
  return discard_count


def main():
  global K, H, T, D
  _, K, H, T, D = map(int, input().split())  # K: 現在持っている絵の具の数, H: 作成すべき色の数, 最大ターン数, 絵の具1グラムのコスト
  owm_list = [list(map(float, input().split())) for _ in range(K)]  # 現在持っている絵の具の色のCMY値
  target_list = [list(map(float, input().split())) for _ in range(H)]  # 作成すべき色のCMY値

  global well_size, wells_num
  well_size = 2  # ウェルの1辺の長さ
  wells_num = N**2 // well_size**2  # ウェルの数
  ic(wells_num)

  palette = [[0, 0.0, 0.0, 0.0] for _ in range(wells_num)]  # パレットの絵の具の量(int)とCMY値(float, float, float)

  # 仕切りをすべて0に初期化
  v_list = [[0]*(N-1) for _ in range(N)]  # v_list[i][j]: マス(i, j)とマス(i, j+1)の間の仕切りの有無
  h_list = [[0]*(N) for _ in range(N-1)]  # h_list[i][j]: マス(i, j)とマス(i+1, j)の間の仕切りの有無

  for j in range(N-1):
    if (j+1) % well_size == 0:
      for i in range(N):
        v_list[i][j] = 1
        h_list[j][i] = 1

  ans_list = []  # 出力する文字列を改行区切りで格納
  total_score = 1  # 最終的なスコア
  total_diff = 0  # diffの合計
  add_count = 0  # 絵の具を出した回数

  for i in range(N):
    ans_list.append(v_list[i])
  for i in range(N-1):
    ans_list.append(h_list[i])

  # ランダムに絵の具を出す
  # 1ウェルあたりの総量から2を引いた値を初期状態の絵の具の量とする
  for i in range(wells_num):
    for _ in range(well_size**2 - 2):
      paint_index = random.randint(0, K-1)
      paint = owm_list[paint_index]
      add_to_palette(palette, i, paint, 1)
      ans_list.append(add_paint(i, paint_index))
      add_count += 1  # add_countのインクリメントをここに移動

  # add_count += 1  # 初期状態で出した絵の具の数
  trans_prob = 1 - (1/wells_num)**(1/wells_num)

  # すべての目標色に対して繰り返し
  for target_index, target in enumerate(target_list):
    trans_count = 0  # コストが同じ場合の遷移が行われた回数
    j_start = 0  # jの開始値

    min_tmp_cost = 10**9
    best_tmp_palette = []
    best_extract_well = -1
    best_command = []
    best_j = -1
    best_diff = 0
    best_discard_count = 0
    best_well_index = -1
    # すべてのウェルに対して
    for well_index in range(wells_num):
      # すべての絵の具に対して
      for i, owm in enumerate(owm_list):
        # 1回または2回絵の具を出す
        for j in range(j_start, 3):
          # パレットのコピー
          tmp_palette = [p[:] for p in palette]
          discard_count = add_to_palette(tmp_palette, well_index, owm, j)
          tmp_command = add_paint(well_index, i)
          # パレットの中で最も近い色を探す
          nearest_index, diff = find_nearest_color(tmp_palette, target)
          # 最小コストを更新
          if D*(j-1) + diff*10**4 <= min_tmp_cost:
            # コストが同じならtrans_prob * (1 - 0.2*trans_count)の確率で遷移
            if D*(j-1) + diff*10**4 == min_tmp_cost:
              if random.random() > trans_prob * (1 - 0.2*trans_count):  # 遷移確率
                continue
              else:
                trans_count += 1  # 遷移が行われた回数をカウント
            min_tmp_cost = D*(j-1) + diff*10**4
            best_command = tmp_command
            best_tmp_palette = tmp_palette
            best_extract_well = nearest_index
            best_j = j
            best_diff = diff
            best_discard_count = discard_count
            best_well_index = well_index

    # 最も近い色を持っている絵の具を提出
    for _ in range(best_discard_count):
      ans_list.append(discard_paint(best_well_index))
    for _ in range(best_j):
      ans_list.append(best_command)
    ans_list.append(extract_color(best_extract_well))
    best_tmp_palette[best_extract_well][0] -= 1  # 絵の具を1グラム減らす
    # if best_tmp_palette[best_extract_well][0] == 0:  # 絵の具がなくなったら0にする
    #   best_tmp_palette[best_extract_well] = [0, 0.0, 0.0, 0.0]
    add_count += best_j
    total_diff += best_diff
    palette = best_tmp_palette  # パレットを更新

  total_score = 1 + D*(add_count - H) + 10**4 * total_diff
  ic(total_score)
  ic(total_diff, add_count)
  # 出力
  for row in ans_list:
    print(*row)

if __name__ == "__main__":
  main()