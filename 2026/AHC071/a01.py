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

W = 80  # 盤面の横幅(固定)
H = 40  # 盤面の縦幅(固定)
K = 120  # 壁に開いている穴の個数(固定)

# NxNの盤面を表現するビットボード(Codonの64bit整数で使えるように改変)
# https://github.com/r-1317/AtCoder/blob/main/library.py 
class BitBoard:
  # N: 盤面のサイズ, board: ビットボードの初期値(指定しない場合はすべて0)
  def __init__(self, N: int, board: List[int] = [0]):
    self.N = N
    # self.board = board
    board = [0] * ((N * N + 63) // 64) if board == [0] else board
    self.board = board

  # (x, y)のマスを1にする
  def set(self, x: int, y: int):
    # self.board |= (1 << (x * self.N + y))
    index = (x * self.N + y) // 64
    bit_position = (x * self.N + y) % 64
    self.board[index] |= (1 << bit_position)

  # (x, y)のマスを0にする
  def unset(self, x: int, y: int):
    # self.board &= ~(1 << (x * self.N + y))
    index = (x * self.N + y) // 64
    bit_position = (x * self.N + y) % 64
    self.board[index] &= ~(1 << bit_position)

  # (x, y)のマスが1かどうかを返す
  def is_set(self, x: int, y: int) -> bool:
    index = (x * self.N + y) // 64
    bit_position = (x * self.N + y) % 64
    return (self.board[index] >> bit_position) & 1 == 1

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
# (ここまで) https://github.com/r-1317/AtCoder/blob/main/library.py

def fill_bricks(hole_bb: BitBoard, brick_bb: BitBoard):
  for y in range(H - 1, -1, -1):  # 上から下に向かって穴の位置を確認する
    for x in range(W):
      if hole_bb.is_set(x, y):  # 穴がある場合
        brick_bb.set(x, y)  # 穴の位置にレンガを置く
      elif y < H - 1 and brick_bb.is_set(x, y + 1):# このマスの上にレンガがある場合
        brick_bb.set(x, y)  # このマスにもレンガを置く

  return brick_bb

def main():
  _, _, _ = map(int, input().split())  # W, H, K の入力を受け取るが、固定値なので無視する
  cost_list = list(map(int, input().split()))  # 各レンガの価格。幅が1, 3, 5, 7, 9のレンガの価格が順に与えられる
  hole_bb = BitBoard(H*W)  # 穴の位置を管理するビットボード。xが横で、yが縦の座標系で表す。(0, 0)が左下
  for _ in range(K):
    x, y = map(int, input().split())
    hole_bb.set(x, y)  # 穴の位置をビットボードにセットする
  brick_bb = BitBoard(H*W)  # そのマスにレンガがあるかを管理するビットボード

  brick_bb = fill_bricks(hole_bb, brick_bb)  # 穴とその下すべてのマスにレンガを置く

  ans_list = []
  for y in range(H):
    for x in range(W):
      if brick_bb.is_set(x, y):  # レンガがある場合
        ans_list.append((x, y, 1))  # その位置に長さ1のレンガを置くことにする

  # 出力
  print(len(ans_list))
  for x, y, l in ans_list:
    print(x, y, l)

if __name__ == "__main__":
  main()