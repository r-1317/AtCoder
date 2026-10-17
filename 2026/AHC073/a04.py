import os
from typing import Tuple, List

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

DIRS = ["D", "U", "R", "L"]

DIR_DICT = {
  "D": (1, 0),
  "U": (-1, 0),
  "R": (0, 1),
  "L": (0, -1)
}

RADIUS_LIMIT = 39**2  # 中心からの距離の二乗が一定以内のマスでのみ魔法陣の使用を許可する

# 魔法陣を使うと、操作前の高橋くんの位置を (i, j)、選んだマスの座標を (a, b) として、高橋くんを (2a−i, 2b−j) へ移す。盤面外への移動はできない。
# 魔法陣を使った場合、操作前の座標(i, j)が新たな魔法陣の座標となる。

def manhattan_distance(pos1: List[int], pos2: List[int]) -> int:
  return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def eauclidean_distance_squared(pos1: List[int], pos2: List[int]) -> int:
  return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2

def get_best_move_02(N: int, K: int, current_pos: List[int], current_goal_pos: List[int], circles: List[List[int]]) -> Tuple[List[str | int], List[int]]:
  best_move = None
  best_score = float('-inf')
  best_new_pos = None

  # 魔法陣を使わない場合の移動
  for dir in DIRS:
    dx, dy = DIR_DICT[dir]
    new_pos = [current_pos[0] + dx, current_pos[1] + dy]
    if 0 <= new_pos[0] < N and 0 <= new_pos[1] < N:
      score = -manhattan_distance(new_pos, current_goal_pos) - eauclidean_distance_squared(new_pos, current_goal_pos) / 1000000  # マンハッタン距離が同じ場合はユークリッド距離の二乗が小さい方を優先する
      if score > best_score:
        best_score = score
        best_move = [dir]
        best_new_pos = new_pos

  # 魔法陣を使う場合の移動
  for i, circle in enumerate(circles):
    if eauclidean_distance_squared(current_pos, [64, 64]) > RADIUS_LIMIT:
      break  # 魔法陣の使用は現在の座標が中心からの距離がRADIUS_LIMIT以内のマスでのみ許可される
    a, b = circle
    new_pos = [2 * a - current_pos[0], 2 * b - current_pos[1]]
    if 0 <= new_pos[0] < N and 0 <= new_pos[1] < N:
      score = -manhattan_distance(new_pos, current_goal_pos) - eauclidean_distance_squared(new_pos, current_goal_pos) / 1000000  # マンハッタン距離が同じ場合はユークリッド距離の二乗が小さい方を優先する
      if score > best_score:
        best_score = score
        best_move = ["J", a, b, i]  # 魔法陣の座標とインデックスを記録
        best_new_pos = new_pos

  return best_move, best_new_pos

def main():
  N, M, K, T = map(int, input().split())  # 盤面の大きさ(128固定)、目的地の数(150固定)、魔法陣の数(3固定)、移動可能な回数
  start = list(map(int, input().split()))  # スタート地点 (x, y)
  goals = [list(map(int, input().split())) for _ in range(M)]  # 目的地の座標 [(x, y), ...]

  circles = [[63, 63], [63, 64], [64, 63]]  # 魔法陣の座標 [(x, y), ...]
  current_pos = start
  current_goal_index = 0
  current_goal_pos = goals[current_goal_index]
  ans_list = []  # 移動の記録を保持する2次元リスト。U, D, L, R 及び魔法陣の使用を記録する。

  # 魔法陣の座標を先に出力する
  for circle in circles:
      print(*circle)

  while current_goal_index < M:
    # 最適な移動を選択する
    best_move, best_new_pos = get_best_move_02(N, K, current_pos, current_goal_pos, circles)

    # 魔法陣をたかった場合は、その座標を更新する
    if len(best_move) == 4:  # 魔法陣を使った場合
      _, a, b, circle_index = best_move
      circles[circle_index] = [current_pos[0], current_pos[1]]  # 魔法陣の座標を更新

    # 現在の位置を更新する
    current_pos = best_new_pos
    ans_list.append(best_move[:3])  # 移動の記録を保持する

    # 目的地に到達した場合、次の目的地に進む
    if current_pos == current_goal_pos:
      current_goal_index += 1
      if current_goal_index < M:
        current_goal_pos = goals[current_goal_index]

  # 出力
  for move in ans_list:
    print(*move)  # 移動の記録を出力

  score = M + T - len(ans_list) + 1
  ic(score)

if __name__ == "__main__":
  main()