import os
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

W = 60  # 盤面の横幅(固定)
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

def calc_score(total_cost: int) -> int:
  return max(0, W * H * 5 - total_cost + 1)  # 総コストが大きいほどスコアは低くなる

def main():
  _, _, _ = map(int, input().split())  # W, H, K の入力を受け取るが、固定値なので無視する
  cost_list = list(map(int, input().split()))  # 各レンガの価格。幅が1, 3, 5, 7, 9のレンガの価格が順に与えられる
  hole_bb = BitBoard(H*W)  # 穴の位置を管理するビットボード。xが横で、yが縦の座標系で表す。(0, 0)が左下
  for _ in range(K):
    x, y = map(int, input().split())
    hole_bb.set(x, y)  # 穴の位置をビットボードにセットする
  brick_bb = BitBoard(H*W)  # そのマスにレンガがあるかを管理するビットボード

  total_cost = 0  # レンガの総コスト
  ans_list = []  # 最終的に出力するレンガの配置を格納するリスト。(x, y, l)のタプルのリスト。x, yはレンガの左下の座標、lはレンガの幅

  # 層ごとに、効率よくレンガを配置していく
  """
  ### 方針
  層を左から見ていって、穴があったら、そこから各長さのレンガを短い方から試す。
  そのレンガで覆える穴の数が今までの穴の数よりも多い場合は、そのレンガに更新する。
  こうして最も穴を塞げるレンガを置いていく。
  穴の割合の仕組みは念の為残しておく。でもしきい値を0.0にして機能しないようにしている。
  置かれたレンガの中心の下のマスに、新たな穴を開ける。
  これを繰り返す。
  """
  for y in range(H - 1, -1, -1):  # 上から下に向かってレンガを配置していく
    for x in range(W):
      if brick_bb.is_set(x, y):  # すでにレンガが置かれている場合はスキップ
        continue
      if hole_bb.is_set(x, y):  # 穴がある場合は、そこからレンガを置く
        max_hole_count = 0  # 覆える穴の最大数
        best_l = 1  # 覆える穴の最大数を得られる
        for l in [1, 3, 5, 7, 9]:  # レンガの長さを短い方から試す
          if x + l > W:  # レンガが盤面からはみ出す場合はスキップ
            continue
          # レンガを置いたときに覆える穴の数を数える
          hole_count = sum(hole_bb.is_set(x + i, y) for i in range(l))
          if hole_count > max_hole_count and hole_count / l >= 0.23:  # 覆える穴の数が最大で、かつ穴の割合がしきい値以上の場合
            max_hole_count = hole_count
            best_l = l

        # 最も穴を塞げるレンガを置く
        for i in range(best_l):
          brick_bb.set(x + i, y)  # レンガを置く
        total_cost += cost_list[(best_l - 1) // 2]  # レンガのコストを加算
        ans_list.append((x, y, best_l))  # レンガの配置を記録
        # レンガの中心の下のマスに新たな穴を開ける
        center_x = x + best_l // 2
        if y > 0:  # 下のマスが存在する場合のみ穴を開ける
          hole_bb.set(center_x, y - 1)
  # 出力
  score = calc_score(total_cost)
  ic(score)
  print(len(ans_list))
  for x, y, l in ans_list:
    print(x, y, l)

if __name__ == "__main__":
  main()