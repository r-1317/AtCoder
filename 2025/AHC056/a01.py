import os
from typing import Tuple, List

from collections import deque

MyPC = os.path.basename(__file__) != "Main.py"
MyPC = False  # 強制的にFalseにする場合はこちらを有効化
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# 最短経路を求める関数
def find_shortest_path(start: Tuple[int, int], goal: Tuple[int, int], vertical_walls: List[List[int]], horizontal_walls: List[List[int]], N: int) -> List[Tuple[int, int]]:

  directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
  queue = deque([start])
  visited = {start: None}  # 各位置の親ノードを記録

  while queue:
    current = queue.popleft()
    if current == goal:
      break

    x, y = current
    for dx, dy in directions:
      nx, ny = x + dx, y + dy
      if 0 <= nx < N and 0 <= ny < N:
        # 壁のチェック
        # ic(dx, dy, x, y, nx, ny)
        if dx == 1 and horizontal_walls[x][y] == 1:  # 下に移動
          continue
        if dx == -1 and horizontal_walls[nx][y] == 1:  # 上に移動
          continue
        if dy == 1 and vertical_walls[x][y] == 1:  # 右に移動
          continue
        if dy == -1 and vertical_walls[x][ny] == 1:  # 左に移動
          continue

        next_pos = (nx, ny)
        if next_pos not in visited:
          visited[next_pos] = current
          queue.append(next_pos)

  # 経路の復元
  path = []
  step = goal
  while step is not None:
    path.append(step)
    step = visited[step]
  path.pop()  # スタート地点は含む必要がないので除外
  path.reverse()  # 逆順にする
  
  return path

# 経路を方向のリストに変換する関数
def path_to_directions(path: List[Tuple[int, int]]) -> List[str]:
  directions = []
  for i in range(1, len(path)):
    x1, y1 = path[i - 1]
    x2, y2 = path[i]
    if x2 == x1 + 1 and y2 == y1:
      directions.append("D")  # Down
    elif x2 == x1 - 1 and y2 == y1:
      directions.append("U")  # Up
    elif x2 == x1 and y2 == y1 + 1:
      directions.append("R")  # Right
    elif x2 == x1 and y2 == y1 - 1:
      directions.append("L")  # Left
    else:
      raise ValueError("Invalid path step")  # 不正な経路ステップ
  return directions

def main():
  N, K, T = map(int, input().split())  # N: 盤面の大きさ, K: 目的地の数, T: 最大の移動回数
  # 壁の情報を受け取る
  str_vertical_walls = [list(input()) for _ in range(N)]  # "0010...0" の形の文字列をlistに変換
  str_horizontal_walls = [list(input()) for _ in range(N - 1)]  # N-1行
  # 目的地の情報を受け取る
  destinations = [tuple(map(int, input().split())) for _ in range(K)]  # (x, y)

  # 壁の情報を整数型に変換
  vertical_walls = [[int(cell) for cell in row] for row in str_vertical_walls]
  horizontal_walls = [[int(cell) for cell in row] for row in str_horizontal_walls]

  grid = [[0] * N for _ in range(N)]  # 盤面の初期化。int型の配列だと非効率な気もするが、一旦はこれで。

  current_position = destinations.pop(0)  # 最初の目的地がスタート地点

  # 最短経路を求める
  path = [current_position]  # スタート地点はあらかじめ含めておく

  # 目的地ごとに最短経路を計算
  for dest in destinations:
    segment_path = find_shortest_path(current_position, dest, vertical_walls, horizontal_walls, N)
    path.extend(segment_path)  # 計算量がO(N^2)なので、後ほど最適化を考える
    current_position = dest

  # 経路を方向のリストに変換
  directions = path_to_directions(path)

  # 出力
  c = 1  # 色の数
  q = len(directions)  # 内部状態の数は経路の長さ
  m = len(directions)  # 出力する命令の数も経路の長さ
  print(c, q, m)

  # 初期の色配置を出力
  for row in grid:
    print(*row)

  # 内部状態遷移と出力命令を出力
  for state in range(m):
    next_state = state + 1 if state + 1 < q else 0  # 最後は状態0に戻る
    print(0, state, 0, next_state,  directions[state])  # [現在の色, 現在の状態, 次の色, 次の状態, 動き]


if __name__ == "__main__":
  main()