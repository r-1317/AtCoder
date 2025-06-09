import os
from typing import Tuple, List
import math
import random
import time
import sys

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
start_time = time.time()  # 開始時刻を記録

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

# prev_state_indexをたどる関数
def collect_state_indices(final_state_index: int, state_list: List[List]) -> List[int]:
  state_index_list = []
  current_index = final_state_index
  while current_index is not None:
    state_index_list.append(current_index)
    current_index = state_list[current_index][6]  # 前の状態のindexを取得
  state_index_list.reverse()  # 最初から最後までの順番にする
  return state_index_list

# コマンドをまとめる関数
def collect_commands(state_index_list: List[int], state_list: List[List]) -> List[List[str]]:
  ans_list = []
  for state_index in state_index_list:
    tmp_ans_list = state_list[state_index][5]  # コマンドリストを取得
    # コマンドを1つずつ追加
    for command in tmp_ans_list:
      ans_list.append(command)  # コマンドを追加
  return ans_list

# diffの合計を計算する関数
def sum_diff(state_index_list: List[int], state_list: List[List]) -> float:
  total_diff = 0.0
  for state_index in state_index_list:
    total_diff += state_list[state_index][2]  # diffを取得して合計
  return total_diff

# add_countの合計を計算する関数
def sum_add_count(state_index_list: List[int], state_list: List[List]) -> int:
  total_add_count = 0
  for state_index in state_index_list:
    total_add_count += state_list[state_index][3]  # add_countを取得して合計
  return total_add_count

def main():
  global K, H, T, D
  _, K, H, T, D = map(int, input().split())  # K: 現在持っている絵の具の数, H: 作成すべき色の数, 最大ターン数, 絵の具1グラムのコスト
  owm_list = [list(map(float, input().split())) for _ in range(K)]  # 現在持っている絵の具の色のCMY値
  target_list = [list(map(float, input().split())) for _ in range(H)]  # 作成すべき色のCMY値

  global well_size, wells_num
  well_size = 4  # ウェルの1辺の長さ
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

  initial_ans_list = []  # 出力する文字列を改行区切りで格納
  # total_score = 1  # 最終的なスコア
  # total_diff = 0  # diffの合計
  initial_add_count = 0  # 絵の具を出した回数

  for i in range(N):
    initial_ans_list.append(v_list[i])
  for i in range(N-1):
    initial_ans_list.append(h_list[i])

  # ランダムに絵の具を出す
  # 1ウェルあたりの総量の1/4の値を初期状態の絵の具の量とする
  for i in range(wells_num):
    for _ in range(well_size**2//4):
      paint_index = random.randint(0, K-1)
      paint = owm_list[paint_index]
      add_to_palette(palette, i, paint, 1)
      initial_ans_list.append(add_paint(i, paint_index))
      initial_add_count += 1  # 絵の具を出した回数をカウント

  # trans_prob = 1 - (1/wells_num)**(1/wells_num)
  boost_limit = 900  # 目標色のうち、indexがboost_limitを超えるものには絵の具を追加しない選択肢を追加する

  # chokudaiサーチ
  chokudai_list = [[] for _ in range(H+1)]  # 色(i-1)を提出したあとの状態のidをソートして格納
  # 盤面の状態を順番に関係なく保存する配列
  state_list = []  # [visited(bool),total_tmp_cost, diff, add_count, [palette], [tmp_ans_list], 前の状態のindex]
  # 初期状態を追加
  state_list.append([False, 0, 0, initial_add_count, palette, initial_ans_list, None])
  chokudai_list[0].append(0)  # 初期状態のidを追加

  # 制限時間まで繰り返し
  while time.time() - start_time < 2.75:
  # すべての目標色に対して繰り返し
    for target_index, target in enumerate(target_list):
      # 次に探索すべき状態を取得
      prev_state_index, palette = chokudai_list[target_index][0], state_list[chokudai_list[target_index][0]][4]
      # 取得した状態のvisitedをTrueにする
      state_list[prev_state_index][0] = True


      # target_indexがboost_limitより大きい場合は、絵の具の追加をしない選択肢を追加
      if boost_limit < target_index:
        # 追加しない選択肢を追加
        tmp_palette = [p[:] for p in palette]
        nearest_index, tmp_diff = find_nearest_color(tmp_palette, target)
        tmp_cost = D * (0 - 1) + tmp_diff * 10**4 + random.uniform(0.0, 0.001)  # ランダムな値を追加して同じコストの状態が複数できるのを防ぐ
        tmp_ans_list = []
        tmp_ans_list.append(extract_color(nearest_index))  # 提出するコマンドを追加
        # 提出した色の絵の具を1グラム減らす
        tmp_palette[nearest_index][0] -= 1
        tmp_add_count = 0
        state_list.append([False, tmp_cost, tmp_diff, tmp_add_count, tmp_palette, tmp_ans_list, prev_state_index])
        chokudai_list[target_index + 1].append(len(state_list) - 1)  # 新しい状態のidを追加

      # すべてのウェルに対して
      for well_index in range(wells_num):
        # すべての絵の具に対して
        for i, owm in enumerate(owm_list):
          # 1回または2回絵の具を出す
          for j in range(1, 3):
            # パレットのコピー
            tmp_palette = [p[:] for p in palette]
            discard_count = add_to_palette(tmp_palette, well_index, owm, j)
            tmp_command = add_paint(well_index, i)
            # パレットの中で最も近い色を探す
            nearest_index, tmp_diff = find_nearest_color(tmp_palette, target)
            # コストを計算
            tmp_cost = D*(j-1+discard_count) + tmp_diff*10**4 + random.uniform(0.0, 0.001)  # ランダムな値を追加して同じコストの状態が複数できるのを防ぐ

            # tmp_ans_listを作成
            tmp_ans_list = []
            for _ in range(discard_count):
              tmp_ans_list.append(discard_paint(well_index))
            for _ in range(j):
              tmp_ans_list.append(tmp_command)
            tmp_ans_list.append(extract_color(nearest_index))

            # 提出した色の絵の具を1グラム減らす
            tmp_palette[nearest_index][0] -= 1

            tmp_add_count = j
            # 状態を追加
            state_list.append([False, tmp_cost, tmp_diff, tmp_add_count, tmp_palette, tmp_ans_list, prev_state_index])
            # chokudai_listに追加
            chokudai_list[target_index + 1].append(len(state_list) - 1)  # 新しい状態のidを追加

      # chokudai_listの状態をソート
      chokudai_list[target_index + 1].sort(key=lambda x: (state_list[x][0], state_list[x][1]))

  # 最後の状態を取得
  final_state_index = chokudai_list[H][0]
  final_state = state_list[final_state_index]

  # prev_state_indexをたどる
  state_index_list = collect_state_indices(final_state_index, state_list)
  ic(state_index_list)

  # コマンドをまとめる
  ans_list = collect_commands(state_index_list, state_list)

  # total_adiff, total_add_countを計算
  total_diff = sum_diff(state_index_list, state_list)
  add_count = sum_add_count(state_index_list, state_list)

  total_score = round(1 + D*(add_count - H) + 10**4 * total_diff)
  ic(total_score)
  print(total_score, file=sys.stderr)  # 標準エラー出力
  ic(total_diff, add_count)
  # 出力
  for row in ans_list:
    print(*row)

  # ここからデバッグ用
  # debug_palette_index = state_index_list[919]
  # debug_palette = state_list[debug_palette_index][4]
  # print("Debug Palette:")
  # for i, paint in enumerate(debug_palette):
  #   print(f"Well {i}: Amount: {paint[0]}, CMY: {paint[1]:.2f}, {paint[2]:.2f}, {paint[3]:.2f}")

if __name__ == "__main__":
  main()