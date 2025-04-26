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

# move: (現在の座標, 次の座標) -> (移動方向, 移動先の座標)
def move(current_coord: list[int, int], next_coord: list[int, int]) -> Tuple[Tuple[str, str], list[int, int]]:
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

def main():
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

  # 障害物を設置せず、1歩ずつ移動する
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
      ans_list.append(next_moove)

  # 回答を出力
  for ans in ans_list:
    print(*ans)

if __name__ == "__main__":
  main()