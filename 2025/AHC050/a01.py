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
        cells.append((i-1, j-1))
  return cells

# func01関数はグリッドとN, Mを受け取り、解答の座標リストを返す
def func01(grid: List[List[int]], N: int, M: int) -> List[Tuple[int, int]]:
  ans_list = []  # 解答の座標リスト
  remaining = N**2 - M  # 残りの空きマスの数
  cells = empty_cells(grid, N)  # 空きマスのリストを取得

  # 残りの空きマスがある限り、1つずつ埋める
  while remaining > 0:
    # 周囲のマスにある岩の数をカウントする変数
    # celsを周りの石の数が多い順にソートする
    cells.sort(key=lambda cell: count_surrounding_rocks(grid, cell[0], cell[1]), reverse=True)
    # ic(cells[0], cells[-1])  # 最も周りの岩が多いマスと少ないマスをデバッグ出力

    # 一番うしろ、つまり周りの岩の数が最も少ないマスを選ぶ
    x, y = cells.pop()  # 最後の空きマスを取得
    ans_list.append((x, y))  # 解答リストに追加
    grid[x][y] = 1  # グリッドに岩を置く
    remaining -= 1  # 残りの空きマスを減らす

  return ans_list  # 解答の座標リストを返す


def main():
  N, M = map(int, input().split())  # Nは40固定、 MはN^2/10以上N^2/4以下の整数
  grid = init_grid(N)  # グリッドの初期化

  # for g in grid:
  #   print(*g)  # グリッドの状態を出力（デバッグ用）

  # ans_listはList[Tuple[int, int]]型で、各タプルは(行, 列)を表す
  ans_list = func01(grid, N, M)  # func01はグリッドとN, Mを受け取り、解答の座標リストを返す

  # 出力形式に合わせて座標を出力
  for i in range(N**2 - M):
    print(ans_list[i][0], ans_list[i][1])  # 各座標を1行ずつ出力



if __name__ == "__main__":
  main()