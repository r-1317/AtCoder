import os
import sys
from typing import Tuple, List

MyPC = os.path.basename(__file__) != "Main.py"
# MyPC = False
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 20  # 固定

# 高橋くんの現在位置から目標位置へ移動するための一歩を決定する。
def step_to(takahashi: List[int], target: Tuple[int, int]) -> Tuple[str, List[int]]:
  if takahashi[0] < target[0]:  # 下に移動
    takahashi[0] += 1
    return "D", takahashi
  elif takahashi[0] > target[0]:  # 上に移動
    takahashi[0] -= 1
    return "U", takahashi
  elif takahashi[1] < target[1]:  # 右に移動
    takahashi[1] += 1
    return "R", takahashi
  elif takahashi[1] > target[1]:  # 左に移動
    takahashi[1] -= 1
    return "L", takahashi
  else:  # 到達済み
    return "", takahashi

# 高橋くんが目標位置に到達するまでの動きをリストで返す。
def move_to(takahashi: List[int], target: Tuple[int, int], carrying_list: List[List[int]]) -> Tuple[List[str], List[int], List[List[int]]]:
  ans = []
  # 目標位置に到達するまでループ
  while takahashi[0] != target[0] or takahashi[1] != target[1]:
    step, takahashi = step_to(takahashi, target)
    ans.append(step)  # 動きを追加
  # 持っているダンボール箱の耐久値を更新
  tmp_wheight = 0
  for i in range(len(carrying_list)-1, -1, -1):
    carrying_list[i][1] -= tmp_wheight * len(ans)  # 耐久値を更新
    tmp_wheight += carrying_list[i][0]  # 重さを加算
  return ans, takahashi, carrying_list  # 動きと現在位置と持っているダンボール箱のリストを返す

# ダンボール箱のインデックスを座標に変換する関数
def index_to_coord(index: int) -> Tuple[int, int]:
  return index // N, index % N

# 耐久値が最大のダンボール箱を探す関数
def find_toughest(d_list: List[List[int]], index_sorted_d: List[int], is_box_removed: List[bool]) -> Tuple[int, int]:
  for index in index_sorted_d:
    if not is_box_removed[index]:  # 取り除かれていないダンボール箱を見つける
      coord = index_to_coord(index)
      return coord  # 座標を返す
  return -1, -1  # 全てのダンボール箱が取り除かれた場合

# ダンボール箱を持ち上げる関数
def pick_up_box(ans_list: List[str], w_list: List[List[int]], d_list: List[List[int]], takahashi: List[int], carrying_list: List[List[int]], is_box_removed: List[bool]) -> None:
  if w_list[takahashi[0]][takahashi[1]] > 0:  # ダンボール箱がある場合
    ans_list.append("1")  # ダンボール箱を持ち上げる
    carrying_list.append([w_list[takahashi[0]][takahashi[1]], d_list[takahashi[0]][takahashi[1]]])  # 重さと耐久値を追加
    # w_list[takahashi[0]][takahashi[1]] = 0  # ダンボール箱を取り除く
    # d_list[takahashi[0]][takahashi[1]] = 0  # 耐久値も0にする
    is_box_removed[takahashi[0] * N + takahashi[1]] = True  # 取り除かれたフラグを立てる
  else:
    ans_list.append("")
    print(f"({takahashi[0]}, {takahashi[1]})のダンボール箱は取り除かれています", file=sys.stderr)
  return None

#原点までのマンハッタン距離
def manhattan_distance(coord: Tuple[int, int]) -> int:
  return abs(coord[0]) + abs(coord[1])

# 上に積めるダンボールの重量の上限を計算する関数
def calc_max_weight(carrying_list: List[List[int]], takahashi: List[int]) -> int:
  dist = manhattan_distance(takahashi)  # 原点までのマンハッタン距離
  min_hp = 10**9
  tmp_wheight = 0
  for i in range(len(carrying_list)-1, -1, -1):
    hp = carrying_list[i][1] - tmp_wheight * dist
    min_hp = min(min_hp, hp)
    tmp_wheight += carrying_list[i][0]  # 重さを加算
  max_weight = min_hp // dist  # 小数点以下は切り捨て。正確な値ではない
  return max_weight

# 寄り道できる位置の上に積めるダンボールのうち、最も原点の遠くにあるものを1つ選ぶ関数
def find_best_box(is_box_removed: List[bool], max_weight: int, takahashi: List[int], w_list: List[List[int]], d_list: List[List[int]]) -> Tuple[int, int]:
  best_coord = (-1, -1)
  best_score = -10**9
  max_x, max_y = takahashi
  for i in range(max_x + 1):
    for j in range(max_y + 1):
      if not is_box_removed[i * N + j] and d_list[i][j] < max_weight:  # 取り除かれていないダンボール箱で、上に積めるもの
        score = vf04((i, j), w_list, d_list)  # 評価関数を計算
        if score > best_score:  # 評価関数の値が最大のものを選ぶ
          best_score = score
          best_coord = (i, j)
  return best_coord

# 04の評価関数
def vf04(coord: Tuple[int, int], w_list: List[List[int]], d_list: List[List[int]]) -> float:
  x, y = coord
  w = w_list[x][y]  # 重さ
  d = d_list[x][y]  # 耐久値
  return w / d  # 耐久値/重さの比率を評価関数とする

def main():
  _ = input()  # Nの入力だが、0で固定
  w_list = [list(map(int, input().split())) for _ in range(N)]  # 重さのリスト
  d_list = [list(map(int, input().split())) for _ in range(N)]  # 耐久値のリスト

  takahashi = [0, 0]  # 高橋くんの位置
  ans_list = []  # 動きのリスト
  remove_count = 0  # 取り除いたダンボール箱の数
  index_sorted_d = list(range(N * N))  # ダンボール箱のインデックスをソートするためのリスト
  index_sorted_d.sort(key=lambda x: d_list[x // N][x % N], reverse=True)  # 耐久値が大きい順にソート
  is_box_removed = [False] * (N * N)  # ダンボール箱が取り除かれたかどうかのフラグ
  is_box_removed[0] = True  # (0, 0)のダンボール箱は最初から取り除かれている
  carrying_list = []  # 高橋くんが持っているダンボール箱の重さと耐久値のリスト。[int, int]

  # 全てのダンボール箱を取り除くまでループ
  while remove_count < N**2 - 1:
    # 耐久値が最大のダンボール箱を探す
    target = find_toughest(d_list, index_sorted_d, is_box_removed)
    # targetまで向かう
    move, takahashi, carrying_list = move_to(takahashi, target, carrying_list)
    ans_list.extend(move)  # 動きを追加
    pick_up_box(ans_list, w_list, d_list, takahashi, carrying_list, is_box_removed)  # ダンボール箱を持ち上げる
    # 寄り道できる位置の上に積めるダンボールのうち、最も評価関数の値が大きいものを1つ選ぶ
    while target != (-1, -1):  # 積める箱が見つからなくなるまで
      max_weight = calc_max_weight(carrying_list, takahashi)  # 上に積めるダンボールの重量の上限
      target = find_best_box(is_box_removed, max_weight, takahashi, w_list, d_list)
      if target != (-1, -1):  # 寄り道できる箱が見つかった場合
        # 寄り道できる位置まで向かう
        move, takahashi, carrying_list = move_to(takahashi, target, carrying_list)
        ans_list.extend(move)
        pick_up_box(ans_list, w_list, d_list, takahashi, carrying_list, is_box_removed)
    # 原点に戻るための動きを追加
    target = (0, 0)
    move, takahashi, carrying_list = move_to(takahashi, target, carrying_list)
    ans_list.extend(move)
    remove_count += len(carrying_list)  # 持っているダンボール箱の数を更新
    carrying_list = []  # 持っているダンボール箱を空にする

  # 出力
  for ans in ans_list:
    if ans:  # 空文字列でない場合のみ出力
      print(ans)
    else:  # 空文字列は標準エラー出力
      print("空文字列", file=sys.stderr)

  # MyPCのみ、総スコアを出力
  if MyPC:
    t = 0
    for ans in ans_list:
      if ans == "U" or ans == "D" or ans == "L" or ans == "R":
        t += 1
    total_score = N**2 + 2 * N**3 - t  # スコア計算
    print(f"総スコア: {total_score}", file=sys.stderr)

if __name__ == "__main__":
  main()