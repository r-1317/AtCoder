import os
import time

# デバッグ用  気にしなくていい
MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# 概要
# 20x20のグリッドが与えられる
# このグリッドの中に、"o" と "x" がある
# "o" は福、"x" は鬼を表す
# 行または列をベルトコンベアのように動かし、鬼をすべて落とす
# ただし、福を落としてはいけない
# 操作の回数は少ないほど良い
# その時の動作を出力する

N = 20

# 鬼を数える
def count_x(grid):
  count = 0
  for i in range(N):
    for j in range(N):
      if grid[i][j] == "x":
        count += 1
  return count

# 福を数える
def count_o(grid):
  count = 0
  for i in range(N):
    for j in range(N):
      if grid[i][j] == "o":
        count += 1
  return count

# 1行または1列を動かした時の結果を返す
def move(grid, d, p):  # grid: 盤面, d: 方向, p: 位置
  new_grid = [row[:] for row in grid]  # deepcopy
  # 左方向の場合
  if d == "L":
    for i in range(N-1):
      new_grid[p][i] = grid[p][i+1]
    new_grid[p][N-1] = "."  # 一番右の列は空白にする
  # 右方向の場合
  elif d == "R":
    new_grid[p][0] = "."  # 一番左の列は空白にする
    for i in range(1, N):
      new_grid[p][i] = grid[p][i-1]
  # 上方向の場合
  elif d == "U":
    for i in range(N-1):
      new_grid[i][p] = grid[i+1][p]
    new_grid[N-1][p] = "."  # 一番下の行は空白にする
  # 下方向の場合
  elif d == "D":
    new_grid[0][p] = "."  # 一番上の行は空白にする
    for i in range(1, N):
      new_grid[i][p] = grid[i-1][p]
  return new_grid

# 鬼が落ちるまでの距離の3乗の逆数を計算
def calc_x_eval(grid, i, j):
  eval = 0
  # 上下左右の4方向に対して
  for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    x = i
    y = j
    flag = False
    dist = 1
    x += di
    y += dj
    # 鬼が落ちるまでの距離を計算
    while 0 <= x < N and 0 <= y < N:
      if grid[x][y] == "o":
        flag = True
        break
      if grid[x][y] == ".":
        dist += 1
      x += di
      y += dj
    # 福がある場合はその経路は通らない
    if flag:
      continue
    # 評価値を計算し、大きい方を採用
    eval = max(eval, 1/dist**3)
  return eval

# 評価値を計算する
def calc_eval_01(grid):
  eval = 0
  # 福を落とした場合、-10**9
  eval -= 10**9 * (2*N - count_o(grid))
  # 鬼を落とした場合、+10**5
  eval += 10**5 * (2*N - count_x(grid))
  # 各鬼に対し、その鬼が落ちるまでの距離を計算
  # 距離の3乗の逆数を評価値に加算
  # ただし、福がある場合はその経路は通らない
  for i in range(N):
    for j in range(N):
      if grid[i][j] == "x":
        eval += calc_x_eval(grid, i, j)
  return eval

# 貪欲法で解く  # もう使わない関数
# def serch_01(grid, ans_list):
#   max_eval = -10**18
#   max_grid = []
#   max_move = ()
#   # 1行または1列を動かす
#   for d in ["L", "R", "U", "D"]:
#     for p in range(N):
#       new_grid = move(grid, d, p)
#       # 評価値を計算
#       eval = calc_eval_01(new_grid)
#       # 評価値が最大の時
#       if max_eval < eval:
#         max_eval = eval
#         max_grid = new_grid
#         max_move = (d, p)
#   # 結果を保存
#   ans_list.append(max_move)
#   # 鬼が1つもなくなったら終了
#   if count_x(max_grid) == 0:
#     return ans_list
#   # 操作回数が4*N^2回になっても終了
#   elif len(ans_list) == 4*N**2:
#     return ans_list
#   # 次の手を探す
#   return serch_01(max_grid, ans_list)

# chokudaiサーチで解く
# 再起のやり方がわからないので、for文で書く
def serch_02(grid, start_time):
  shortest_ans_list = []  # 最短の操作
  min_len = 4*N**2+1  # 最短の操作回数
  chokudai_list = [[] for _ in range(4*N**2+1)]  # chokudaiサーチのための、盤面のリスト。操作回数ごとに保存
  # 最初の盤面について、操作回数0のリストに追加
  # その際、評価値とそれまでの操作と探索済みかどうかを保存
  # [探索済みか, 評価値, 盤面, 操作] の順
  eval = calc_eval_01(grid)
  chokudai_list[0].append([False, eval, grid, []])
  # 実行時間が1.9秒以内である限りビームを打ち続ける
  while time.time() - start_time < 1.9:
    # 操作回数ごとに探索
    # 操作回数が最も少ないものを探すため、すでに見つかっている最短の操作回数より多い場合は探索を終了
    for i in range(min_len-1):
      flag = False  # 最短の操作が見つかったかどうか
      # 探索済みでない盤面について
      # 探索済みでない盤面のうち、最も評価値が高いものを探索
      if chokudai_list[i][0][0]:
        continue
      # すべての操作について、次の盤面を探索
      for d in ["L", "R", "U", "D"]:
        # 最短の操作がすでに見つかっている場合、探索を終了
        if flag:
          break
        for p in range(N):
          new_grid = move(chokudai_list[i][0][2], d, p)
          # 評価値を計算
          eval = calc_eval_01(new_grid)
          # ここまでの操作を記録
          operation_list = chokudai_list[i][0][3][:] + [(d, p)]
          # chokudai_listに追加
          chokudai_list[i+1].append([False, eval, new_grid, operation_list])
          # 鬼がすべて落ちた場合、ビームを打ち切る
          if count_x(new_grid) == 0:
            # 最短の操作回数を更新
            min_len = i+1
            shortest_ans_list = operation_list
            flag = True
            break
      # 今追加した階層について、未探索のものを優先して、評価値が高い順にソート
      chokudai_list[i+1].sort(key=lambda x: (x[0], -x[1]))
      # 探索済みにする
      chokudai_list[i][0][0] = True
      # 最短の操作がすでに見つかっている場合、探索を終了
      if flag:
        break
  # 結果を返す
  return shortest_ans_list

def main():
  start_time = time.time()  # 開始時刻
  n = int(input())  # 20固定
  grid = [[""]*N for _ in range(N)]  # 20x20のグリッド
  # 20行分の入力
  # "o": 福, "x": 鬼, ".": 何もない
  for i in range(N):
    s = input()  # "o", "x", "." からなる文字列
    for j in range(N):
      grid[i][j] = s[j]

  # chokudaiサーチで解く
  ans_list = serch_02(grid, start_time)
  # 出力
  # print(len(ans_list))
  for ans in ans_list:
    print(*ans)

if __name__ == "__main__":
  main()