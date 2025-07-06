import os
from typing import Tuple, List
import time
import random

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

T = 1.0  # 制限時間（秒）
start_time = time.time()  # 開始時刻を記録
random.seed(1317)  # 乱数のシードを設定

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

def func03(grid: List[List[int]], N: int, M: int) -> List[Tuple[int, int]]:
  ans_list = []  # 解答の座標リスト
  remaining = N**2 - M  # 残りの空きマスの数
  cells = empty_cells(grid, N)  # 空きマスのリストを取得

  prob_grid = init_prob_grid(grid, N, M)  # 確率グリッドの初期化

  chokudai_list = [[] for _ in range(remaining+1)]  # chokudaiサーチ(ビームサーチの亜種)で使用するリスト
  money = 0  # 賞金の期待値
  live_prob = 1.0  # 生存確率

  state_list = []  # 状態を保存するリスト  [not_visited, money, live_prob, grid, cells, prob_grid, coord, prev_state_index]
  # 初期状態を追加
  state_list.append([True, money, live_prob, grid, cells, prob_grid, None, -1])

  chokudai_list[0].append(0)  # 初期状態を追加  

  # T秒間繰り返し
  while time.time() - start_time < T:
    for i in range(len(chokudai_list)):
      current_state_index = chokudai_list[i][0]  # 現在の状態のインデックスリストを取得
      state = state_list[current_state_index]  # 現在の状態を取得
      # すべて探索済みの場合はスルー
      if not state[0]:  # not_visitedがFalseの場合、つまり探索済みの場合
        continue
      state[0] = False  # 探索済みフラグを立てる

      money, live_prob, grid, cells, prob_grid = state[1:6]  # 状態から必要な情報を取得

      # 2. 確率グリッドを更新
      prob_grid = calc_prob(grid, prob_grid, N)  # 確率グリッドを更新

      # 3. cellsを確率の高い順にソートする
      cells.sort(key=lambda cell: prob_grid[cell[0]][cell[1]], reverse=True)

      cells_tail = cells[len(cells) - (len(cells)//75 + 1):]  # cellsの後ろ1/10を取得  # 1/75に変更

      # 4. cellsの後ろ1/10のそれぞれを選択した場合について、1手先の状態を計算
      for x, y in cells_tail:
        new_grid = [row[:] for row in grid]
        new_grid[x][y] = 1  # グリッドに岩を置く
        new_live_prob = live_prob - prob_grid[x][y]  # 生存確率を更新
        new_money = money + live_prob  # 賞金の期待値を更新
        new_cells = [cell for cell in cells if cell != (x, y)]  # 選択したマスを除外
        coord = (x - 1, y - 1)  # 0-indexedに変換
        # 5. 新しい状態を追加
        new_state = [True, new_money, new_live_prob, new_grid, new_cells, prob_grid, coord, current_state_index]
        state_list.append(new_state)  # 新しい状態を追加
        new_state_index = len(state_list) - 1  # 新しい状態のインデックスを取得
        chokudai_list[i + 1].append(new_state_index)  # 新しい状態のインデックスをchokudai_listに追加
      # 6. chokudai_list[i+1]
      if i != remaining:  # 最後のリスト以外の場合
        chokudai_list[i + 1].sort(key=lambda index: state_list[index], reverse=True)  # visited, money, live_prob の順でソート

  # ここまででchokudaiサーチは終了
  # chokudai_list[-1]をmoney順でソート
  chokudai_list[-1].sort(key=lambda index: state_list[index][1], reverse=True)  # moneyの降順でソート
  # 最もお金の期待値が高い状態を取得
  best_state_index = chokudai_list[-1][0]  # 最もお金の期待値が高い状態のインデックスを取得
  
  ans_list = []  # 解答の座標リスト
  # prev_state_indexをたどって、解答の座標を取得
  current_state_index = best_state_index
  while current_state_index != -1:
    state = state_list[current_state_index]  # 現在の状態を取得
    coord = state[6]  # 座標を取得
    if coord is not None:  # 座標がNoneでない場合
      ans_list.append(coord)  # 解答リストに追加
    current_state_index = state[7]  # 前の状態のインデックスを取得

  ans_list.reverse()  # 解答リストを逆順にする
  return ans_list  # 解答の座標リストを返す

def main():
  N, M = map(int, input().split())  # Nは40固定、 MはN^2/10以上N^2/4以下の整数
  grid = init_grid(N)  # グリッドの初期化

  # for g in grid:
  #   print(*g)  # グリッドの状態を出力（デバッグ用）

  # ans_listはList[Tuple[int, int]]型で、各タプルは(行, 列)を表す
  ans_list = func03(grid, N, M)

  # 出力形式に合わせて座標を出力
  for i in range(N**2 - M):
    print(ans_list[i][0], ans_list[i][1])  # 各座標を1行ずつ出力



if __name__ == "__main__":
  main()