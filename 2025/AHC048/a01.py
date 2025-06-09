import os
from typing import Tuple
import math

debug  = True
# debug = False
MyPC = os.path.basename(__file__) != "Main.py" and debug
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

N = 20  # 固定

ic.enable() if MyPC else None

# 指定された位置(x, y)に、指定されたインデックスの絵の具を追加するコマンドを返す。
def add_paint(x: int, y: int, index: int) -> str:
  return f"1 {x} {y} {index}"

# 指定された位置(x, y)の絵の具を提出するコマンドを返す。
def extract_color(x: int, y: int) -> str:
  return f"2 {x} {y}"

# CMY値の差を計算する関数
def calc_diff(owm: list, target: list) -> float:
  return math.sqrt((target[0] - owm[0]) ** 2 + (target[1] - owm[1]) ** 2 + (target[2] - owm[2]) ** 2)

# 目標色に最も近い色を見つける関数
def find_nearest_color(owm_list: list, target: list) -> Tuple[int, float]:
  nearest_index = -1
  min_diff = 10**9
  for i, owm in enumerate(owm_list):
    diff = calc_diff(owm, target)
    if diff < min_diff:
      min_diff = diff
      nearest_index = i

  return nearest_index, min_diff

def main():
  global K, H, T, D
  _, K, H, T, D = map(int, input().split())  # K: 現在持っている絵の具の数, H: 作成すべき色の数, 最大ターン数, 絵の具1グラムのコスト
  owm_list = [list(map(float, input().split())) for _ in range(K)]  # 現在持っている絵の具の色のCMY値
  target_list = [list(map(float, input().split())) for _ in range(H)]  # 作成すべき色のCMY値

  # 仕切りをすべて0に初期化
  v_list = [[0]*(N-1) for _ in range(N)]  # v_list[i][j]: マス(i, j)とマス(i, j+1)の間の仕切りの有無
  h_list = [[0]*(N-1) for _ in range(N)]  # h_list[i][j]: マス(i, j)とマス(i+1, j)の間の仕切りの有無

  ans_list = []  # 出力する文字列を改行区切りで格納
  total_diff = 0
  cost = 0

  for i in range(N):
    ans_list.append(v_list[i])
  for i in range(N):
    ans_list.append(h_list[i])

  # すべての目標色に対して繰り返し
  for target in target_list:
    # 目標色に最も近い色を持っている絵の具を探す
    nearest_index, diff = find_nearest_color(owm_list, target)
    # その色をマス(0, 0)に出す
    ans_list.append([add_paint(0, 0, nearest_index)])
    cost += 1
    total_diff += diff
    # 出した色をそのまま提出
    ans_list.append([extract_color(0, 0)])

  total_score = 1 + D*(H - cost) + 10**4 * total_diff
  ic(total_score)
  ic(total_diff, cost)
  # 出力
  for row in ans_list:
    print(*row)





if __name__ == "__main__":
  main()