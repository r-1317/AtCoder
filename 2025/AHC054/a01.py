import os
from typing import List, Tuple

MyPC = os.path.basename(__file__) != "Main.py"
MyPC = False
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# NxNの盤面をビットボードで表現する
class BitBoard:
  # N: 盤面のサイズ, board: ビットボードの初期値(指定しない場合はすべて0)
  def __init__(self, N: int, board: int = 0):
    self.N = N
    self.board = board

  # (x, y)のマスを1にする
  def set(self, x: int, y: int):
    self.board |= (1 << (x * self.N + y))

  # (x, y)のマスを0にする
  def unset(self, x: int, y: int):
    self.board &= ~(1 << (x * self.N + y))

  # (x, y)のマスが1かどうかを返す
  def is_set(self, x: int, y: int) -> bool:
    return (self.board >> (x * self.N + y)) & 1 == 1

  # ビットボードを文字列で表示する
  def __str__(self):
    res = []
    for i in range(self.N):
      row = []
      for j in range(self.N):
        if self.is_set(i, j):
          row.append('1')
        else:
          row.append('0')
      res.append(''.join(row))
    return '\n'.join(res)

def main():
  N, tx, ty = map(int, input().split())
  goal = (tx, ty)
  grid = [input() for _ in range(N)]

  current_coord = (0, N//2)  # 直前の座標

  grid_BB = BitBoard(N)
  for i in range(N):
    for j in range(N):
      if grid[i][j] == "T":
        grid_BB.set(i, j)

  tentative_BB = BitBoard(N)  # 確認済みマスを1にするビットボード
  tentative_BB.set(current_coord[0], current_coord[1])

  while True:
    next_coord = tuple(map(int, input().split()))  # 次に移動する座標
    revealed_cells = list(map(int, input().split()))  # 確認済みマスのリスト
    # revealed_cellsの最初の要素は確認済みマスの数
    # 以降の要素は(x1, y1, x2, y2, ..., xk, yk)の形式で与えられる
    for i in range(1, len(revealed_cells), 2):
      x, y = revealed_cells[i], revealed_cells[i+1]
      tentative_BB.set(x, y)
    # 次に移動する座標がゴールなら終了
    if next_coord == goal:
      break
    print(0)
    current_coord = next_coord

if __name__ == "__main__":
  main()