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

# N, M, Kは固定
N = 30  # グリッドの高さ・幅
M = 10  # ロボットの数
K = 10  # キーコンフィグの数

UDLR = ("U", "D", "L", "R")

# 30x30のビットボード
# ロボットが訪れたますかどうかを管理
class BitBoard:
  def __init__(self, *args):
    # 引数があればそれをビットボードとして扱う
    if args:
      self.board = args[0]
      self.visit_count = args[1]
    # ない場合は初期化
    else:
      self.board = 1<<900  # 30x30のビットボード。C++に移植する際は64bit整数15個の配列で扱う
      self.visit_count = 0  # 訪問したマスの数。900ですべてのマスを訪問したことになる

  # ロボットが(x, y)を訪れたことを記録
  def visit(self, x: int, y: int):
    if not self.has_visited(x, y):
      self.visit_count += 1
    self.board |= 1 << (y * 30 + x)

  # (x, y)にロボットが訪れたことがあるか
  def has_visited(self, x: int, y: int) -> bool:
    return (self.board & (1 << (y * 30 + x))) != 0

# 最も少ない手順でたどり着ける未訪問マスを探す
def find_nearest_unvisited(BB: BitBoard, x: int, y: int, X_wall_list: List[List[int]], Y_wall_list: List[List[int]]) -> Tuple[int, int]:
  # BFSのためのキュー
  queue = [(x, y, 0)]  # (x, y, 手数)
  visited = set()
  visited.add((x, y))

  while queue:
    cx, cy, steps = queue.pop(0)

    # 未訪問マスを見つけたら返す
    if not BB.has_visited(cx, cy):
      return (cx, cy)

    # 移動可能な方向を探索
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
      nx, ny = cx + dx, cy + dy

      # 壁がないかつ範囲内であればキューに追加
      if (0 <= nx < 30) and (0 <= ny < 30) and (nx, ny) not in visited:
        if dx == -1 and X_wall_list[nx][ny] == 0:  # 上
          queue.append((nx, ny, steps + 1))
          visited.add((nx, ny))
        elif dx == 1 and X_wall_list[nx-1][ny] == 0:  # 下
          queue.append((nx, ny, steps + 1))
          visited.add((nx, ny))
        elif dy == -1 and Y_wall_list[nx][ny] == 0:  # 左
          queue.append((nx, ny, steps + 1))
          visited.add((nx, ny))
        elif dy == 1 and Y_wall_list[nx][ny-1] == 0:  # 右
          queue.append((nx, ny, steps + 1))
          visited.add((nx, ny))

  return (-1, -1)  # 見つからなかった場合

# 目的地に行くために最適な次のステップを計算
def get_next_step(BB: BitBoard, robot: Tuple[int, int], destination: Tuple[int, int], X_wall_list: List[List[int]], Y_wall_list: List[List[int]]) -> str:
  # BFSで最短経路の最初の一歩を見つける
  rx, ry = robot
  tx, ty = destination

  if rx == tx and ry == ty:
    return "S"  # 既に目的地にいる場合は停止

  queue = [(rx, ry, "")]  # (x, y, 最初の方向)
  visited = set()
  visited.add((rx, ry))

  while queue:
    cx, cy, first_direction = queue.pop(0)
    
    # 目的地に到達したら最初の方向を返す
    if cx == tx and cy == ty:
      return first_direction
    
    # 4方向に移動を試す
    directions = [(0, -1, "L"), (0, 1, "R"), (-1, 0, "U"), (1, 0, "D")]
    
    for dx, dy, direction in directions:
      nx, ny = cx + dx, cy + dy
      
      # 範囲外チェック
      if not (0 <= nx < 30 and 0 <= ny < 30):
        continue
      
      if (nx, ny) in visited:
        continue
      
      # 壁チェック
      can_move = False
      if dx == -1 and X_wall_list[nx][ny] == 0:  # 上
        can_move = True
      elif dx == 1 and X_wall_list[nx-1][ny] == 0:  # 下
        can_move = True
      elif dy == -1 and Y_wall_list[nx][ny] == 0:  # 左
        can_move = True
      elif dy == 1 and Y_wall_list[nx][ny-1] == 0:  # 右
        can_move = True

      if can_move:
        # 最初のステップの場合は方向を記録
        next_first_direction = first_direction if first_direction else direction
        queue.append((nx, ny, next_first_direction))
        visited.add((nx, ny))

  return "S"  # 経路が見つからない場合は停止

# ロボットの動きを反映
def move_robot(BB: BitBoard, robots_list: List[List[int]], key_config: List[List[str]], key: int, X_wall_list: List[List[int]], Y_wall_list: List[List[int]]) -> Tuple[BitBoard, List[List[int]]]:
  for i, (x, y) in enumerate(robots_list):
    direction = key_config[key][i]
    if direction == "U":
      nx, ny = x - 1, y
    elif direction == "D":
      nx, ny = x + 1, y
    elif direction == "L":
      nx, ny = x, y - 1
    elif direction == "R":
      nx, ny = x, y + 1
    else:
      continue

    # 移動先が範囲内かつ壁がない場合に移動
    # ic(x, y, nx, ny, direction)
    if 0 <= nx < 30 and 0 <= ny < 30:
      if direction == "U" and X_wall_list[nx][ny] == 0:
        robots_list[i] = (nx, ny)
        BB.visit(nx, ny)
      elif direction == "D" and X_wall_list[nx-1][ny] == 0:
        robots_list[i] = (nx, ny)
        BB.visit(nx, ny)
      elif direction == "L" and Y_wall_list[nx][ny] == 0:
        robots_list[i] = (nx, ny)
        BB.visit(nx, ny)
      elif direction == "R" and Y_wall_list[nx][ny-1] == 0:
        robots_list[i] = (nx, ny)
        BB.visit(nx, ny)

  return BB, robots_list

def main():
  _, _, _ = map(int, input().split())  # N, M, Kを受け取るが使わない
  robots_list = [list(map(int, input().split())) for _ in range(M)]  # 各ロボットの座標
  # Y_wall_list = [list(map(int, input().split())) for _ in range(N)]  # 左右の移動を阻害する壁の情報
  # X_wall_list = [list(map(int, input().split())) for _ in range(N-1)]  # 上下の移動を阻害する壁の情報
  Y_wall_list = [[int(c) for c in input()] for _ in range(N)]  # 左右の移動を阻害する壁の情報
  X_wall_list = [[int(c) for c in input()] for _ in range(N-1)]  # 上下の移動を阻害する壁の情報
  # ic(len(robots_list), len(X_wall_list[0]), len(Y_wall_list[0]))

  key_config_list = [["S"]*M for _ in range(K)]  # キーコンフィグの情報 U,D,L,Rで上下左右に移動、Sで停止

  key_config_list[0] = ["U"]*M  # 1手目は全ロボットを上に移動
  key_config_list[1] = ["D"]*M  # 2手目は全ロボットを下に移動
  key_config_list[2] = ["L"]*M  # 3手目は全ロボットを左に移動
  key_config_list[3] = ["R"]*M  # 4手目は全ロボットを右に移動

  BB = BitBoard()

  # ロボットの初期位置をビットボードに登録
  for x, y in robots_list:
    BB.visit(x, y)

  ans_list = []

  # 各方向のキー設定
  dir2key = {
    "U": 0,
    "D": 1,
    "L": 2,
    "R": 3,
    "S": 4
  }

  # すべてのマスに訪れるまで繰り返す
  while BB.visit_count < 900:
    nearest_unvisited = find_nearest_unvisited(BB, robots_list[0][0], robots_list[0][1], X_wall_list, Y_wall_list)
    next_step = get_next_step(BB, robots_list[0], nearest_unvisited, X_wall_list, Y_wall_list)
    # ic(robots_list[0], nearest_unvisited, next_step)
    if next_step == "S":
      break
    ans_list.append(dir2key[next_step])
    BB, robots_list = move_robot(BB, robots_list, key_config_list, dir2key[next_step], X_wall_list, Y_wall_list)  # 移動を反映
  
  # 回答を出力
  for key_config in key_config_list:
    print(*key_config)
  for ans in ans_list:
    print(ans)

if __name__ == "__main__":
  main()