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

# グリッドの初期化関数
def init_grid(N: int) -> List[List[int]]:
  grid = [[1] * (N+2) for _ in range(N+2)]  # 1-indexedでN×Nのグリッドを初期化。周りは番兵

  # 入力を1行ずつ受け取る
  for i in range(1, N+1):
    row = list(input())  # "."または"#"の文字列を受け取る
    for j in range(1, N+1):
      if row[j-1] == ".":
        grid[i][j] = 0

  return grid

# 周囲にある岩の数をカウントする関数
def count_surrounding_rocks(grid: List[List[int]], x: int, y: int) -> int:
  count = 0
  # 周囲の4方向をチェック
  for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    nx, ny = x + dx, y + dy
    if grid[nx][ny] == 1:  # 岩がある場合
      count += 1

  return count

# 空きマスのリストを取得する関数
def empty_cells(grid: List[List[int]], N: int) -> List[Tuple[int, int]]:
  cells = []
  for i in range(1, N+1):
    for j in range(1, N+1):
      if grid[i][j] == 0:  # 空きマスの場合
        cells.append((i, j))
  return cells

# 確率グリッドの初期化関数
def init_prob_grid(grid: List[List[int]], N: int, M: int) -> List[List[float]]:
  prob_grid = [[0.0] * (N+2) for _ in range(N+2)]  # 確率グリッドの初期化

  p = 1 / (N**2 - M)  # 最初は空きマスに均等に確率を割り当てる
  for i in range(1, N+1):
    for j in range(1, N+1):
      if grid[i][j] == 0:  # 空きマスの場合
        prob_grid[i][j] = p  # 確率を割り当てる

  return prob_grid

# 確率グリッドを更新する関数
def calc_prob(grid: List[List[int]], prob_grid: List[List[float]], N: int) -> List[List[float]]:
  coord_list = []  # indexを座標に変換するためのリスト
  dst_grid = [[[0]*4 for _ in range(N+2)] for _ in range(N+2)]  # 上下左右の座標のindexを格納するグリッド
  current_index = 0  # いま走査しているマスの集合が止まるマスの座標が入るindex

  # 上下左右それぞれに対し、止まる位置の座標を計算
  # 上方向
  for j in range(1, N+1):
    for i in range(N, 0, -1):
      if grid[i][j] == 1:  # 岩がある場合
        continue  # 岩の中からは進めないので、次のマスへ

      # 岩がない場合、現在のマスのindexを格納
      dst_grid[i][j][0] = current_index  # このマスから上方向に進んだときの止まるマスのindexを格納
      if grid[i-1][j] == 1:  # 次のマスに岩がある場合
        coord_list.append((i, j))  # 現在の座標をリストに追加
        current_index += 1  # 次のマスのindexを更新

  # 下方向
  for j in range(1, N+1):
    for i in range(1, N+1):
      if grid[i][j] == 1:  # 岩がある場合
        continue  # 岩の中からは進めないので、次のマスへ

      # 岩がない場合、現在のマスのindexを格納
      dst_grid[i][j][1] = current_index  # このマスから下方向に進んだときの止まるマスのindexを格納
      if grid[i+1][j] == 1:  # 次のマスに岩がある場合
        coord_list.append((i, j))  # 現在の座標をリストに追加
        current_index += 1  # 次のマスのindexを更新

  # 左方向
  for i in range(1, N+1):
    for j in range(N, 0, -1):
      if grid[i][j] == 1:  # 岩がある場合
        continue  # 岩の中からは進めないので、次のマスへ

      # 岩がない場合、現在のマスのindexを格納
      dst_grid[i][j][2] = current_index  # このマスから左方向に進んだときの止まるマスのindexを格納
      if grid[i][j-1] == 1:  # 次のマスに岩がある場合
        coord_list.append((i, j))  # 現在の座標をリストに追加
        current_index += 1  # 次のマスのindexを更新

  # 右方向
  for i in range(1, N+1):
    for j in range(1, N+1):
      if grid[i][j] == 1:  # 岩がある場合
        continue  # 岩の中からは進めないので、次のマスへ

      # 岩がない場合、現在のマスのindexを格納
      dst_grid[i][j][3] = current_index  # このマスから右方向に進んだときの止まるマスのindexを格納
      if grid[i][j+1] == 1:  # 次のマスに岩がある場合
        coord_list.append((i, j))  # 現在の座標をリストに追加
        current_index += 1  # 次のマスのindexを更新

  new_prob_grid = [[0.0] * (N+2) for _ in range(N+2)]  # 新しい確率グリッドの初期化

  # 確率グリッドを更新
  for i in range(1, N+1):
    for j in range(1, N+1):
      if grid[i][j] == 1:  # 岩がある場合
        new_prob_grid[i][j] = 9.9  # 岩のあるマスは確率を9.9に設定
        continue  # 岩のあるマスは確率を更新しない
      quarter_p = prob_grid[i][j] / 4  # 各方向に進む確率は均等に1/4
      for d in range(4):
        stop_index = dst_grid[i][j][d]
        x, y = coord_list[stop_index]  # 止まるマスの座標を取得
        new_prob_grid[x][y] += quarter_p  # 確率を更新

  return new_prob_grid  # 更新された確率グリッドを返す

def func02(grid: List[List[int]], N: int, M: int) -> List[Tuple[int, int]]:
  ans_list = []  # 解答の座標リスト
  remaining = N**2 - M  # 残りの空きマスの数
  cells = empty_cells(grid, N)  # 空きマスのリストを取得

  prob_grid = init_prob_grid(grid, N, M)  # 確率グリッドの初期化

  # 残りの空きマスがある限り、1つずつ埋める
  while remaining > 0:
    prob_grid = calc_prob(grid, prob_grid, N)  # 確率グリッドを更新
    ic(prob_grid[1][40])

    # cellsを確率の高い順にソートする
    cells.sort(key=lambda cell: prob_grid[cell[0]][cell[1]], reverse=True)
    # ic(cells[0], cells[-1])  # 最も確率の高いマスと低いマスをデバッグ出力

    # 一番うしろ、つまり確率の最も低いマスを選ぶ
    x, y = cells.pop()  # 最後の空きマスを取得
    grid[x][y] = 1  # グリッドに岩を置く
    x, y = x - 1, y - 1  # 0-indexedに変換
    ans_list.append((x, y))  # 解答リストに追加
    remaining -= 1  # 残りの空きマスを減らす

  return ans_list  # 解答の座標リストを返す

def main():
  N, M = map(int, input().split())  # Nは40固定、 MはN^2/10以上N^2/4以下の整数
  grid = init_grid(N)  # グリッドの初期化

  # for g in grid:
  #   print(*g)  # グリッドの状態を出力（デバッグ用）

  # ans_listはList[Tuple[int, int]]型で、各タプルは(行, 列)を表す
  ans_list = func02(grid, N, M)

  # 出力形式に合わせて座標を出力
  for i in range(N**2 - M):
    print(ans_list[i][0], ans_list[i][1])  # 各座標を1行ずつ出力



if __name__ == "__main__":
  main()