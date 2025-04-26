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
# task: https://atcoder.jp/contests/ahc046/tasks/ahc046_a

# move_by_step: (現在の座標, 次の座標) -> (移動方向, 移動先の座標)
def move_by_step(current_coord: list[int, int], next_coord: list[int, int]) -> Tuple[Tuple[str, str], list[int, int]]:
  # x軸正の方向に移動する
  if current_coord[0] < next_coord[0]:
    current_coord[0] += 1
    return ("M", "D"), current_coord
  
  # x軸負の方向に移動する
  elif current_coord[0] > next_coord[0]:
    current_coord[0] -= 1
    return ("M", "U"), current_coord
  
  # y軸正の方向に移動する
  elif current_coord[1] < next_coord[1]:
    current_coord[1] += 1
    return ("M", "R"), current_coord
  
  # y軸負の方向に移動する
  elif current_coord[1] > next_coord[1]:
    current_coord[1] -= 1
    return ("M", "L"), current_coord

  # 現在の座標と次の座標が同じ場合はエラーを返す
  else:
    ic(current_coord, next_coord)
    raise ValueError("Current coordinate and next coordinate are the same")

# move: (現在の座標, 次の座標) -> (移動方向, 移動先の座標)
def move(current_coord: list[int, int], next_coord: list[int, int]) -> Tuple[Tuple[str, str], list[int, int]]:
  # 1歩ずつ移動した場合と、x軸またはy軸の正または負の方向に滑走した場合のコストを計算する
  # 1歩ずつ移動した場合(マンハッタン距離)
  step_cost = abs(current_coord[0] - next_coord[0]) + abs(current_coord[1] - next_coord[1])
  # x軸正の方向に滑走した場合
  skate_D_cost = abs(n - next_coord[0]) + abs(current_coord[1] - next_coord[1]) + 1  # 滑走するため+1
  # x軸負の方向に滑走した場合
  skate_U_cost = abs(1 - next_coord[0]) + abs(current_coord[1] - next_coord[1]) + 1  # 滑走するため+1
  # y軸正の方向に滑走した場合
  skate_R_cost = abs(current_coord[0] - next_coord[0]) + abs(n - next_coord[1]) + 1  # 滑走するため+1
  # y軸負の方向に滑走した場合
  skate_L_cost = abs(current_coord[0] - next_coord[0]) + abs(1 - next_coord[1]) + 1  # 滑走するため+1
  
  # 1歩ずつ移動した場合と、滑走した場合のコストを比較する
  min_cost = min(step_cost, skate_D_cost, skate_U_cost, skate_R_cost, skate_L_cost)
  # 最小コストの動きを選択する
  if min_cost == skate_D_cost:
    # x軸正の方向に滑走する
    current_coord[0] = n
    return ("S", "D"), current_coord
  elif min_cost == skate_U_cost:
    # x軸負の方向に滑走する
    current_coord[0] = 1
    return ("S", "U"), current_coord
  elif min_cost == skate_R_cost:
    # y軸正の方向に滑走する
    current_coord[1] = n
    return ("S", "R"), current_coord
  elif min_cost == skate_L_cost:
    # y軸負の方向に滑走する
    current_coord[1] = 1
    return ("S", "L"), current_coord
  else:
    # 1歩ずつ移動する
    return move_by_step(current_coord, next_coord)


def main():
  global n
  global m
  n, m = map(int, input().split())
  coord_list = [list(map(int, input().split())) for _ in range(m)]

  grid = [[0] * (n+2) for _ in range(n+2)]  # 0なら空きマス、1なら障害物
  # 周囲のマスを障害物にする
  for i in range(n+2):
    grid[i][0] = grid[i][n+1] = 1
  for j in range(n+2):
    grid[0][j] = grid[n+1][j] = 1

  # 座標をすべて+1する
  coord_list = [[x+1, y+1] for x, y in coord_list]

  current_coord = [coord_list[0][0], coord_list[0][1]]  # 現在の座標を初期化

  # 障害物を設置せず、滑走または1歩ずつ移動する
  ans_list = []
  # 1からm-1までの座標を順に移動する
  for i in range(1, m):
    next_coord = coord_list[i]
    # 目的地に到達するまで移動する
    while current_coord != next_coord:
      # ic(current_coord, next_coord)
      # next_moove, current_coord = move(current_coord, next_coord)
      retrun_val = move(current_coord, next_coord)
      # ic(retrun_val)
      next_moove, current_coord = retrun_val
      # try:
      #   next_moove, current_coord = retrun_val
      # except:
      #   ic(current_coord, next_coord)
      #   raise ValueError("Current coordinate and next coordinate are the same")
      ans_list.append(next_moove)

  # 回答を出力
  for ans in ans_list:
    print(*ans)

if __name__ == "__main__":
  main()