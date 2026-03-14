import os
from typing import Tuple, List
import random
import time
import sys

MyPC = os.path.basename(__file__) != "Main.py"
# MyPC = False  # 一時的にデバッグ用のコードを無効化するために、MyPCをFalseに設定する
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

start_time = time.time()

random.seed(1317)

N = 200
TIME_LIMIT = 1.75  # 時間制限（秒）

# 行ごとの合計を計算する関数
def calculate_column_sums(grid: List[List[int]]) -> List[int]:
  """
  行ごとの合計を計算する関数
  ただし、最後の行は除外する
  また、最初と最後の列も計算には含めない
  Args:
    grid: 2次元リストで表されるグリッド
  Returns:
    行ごとの合計を格納したリスト
  """
  column_sums = [0] * N
  for i in range(N - 1):  # 最後の行は除外
    for j in range(1, N - 1):  # 最初と最後の列は除外
      column_sums[j] += grid[i][j]
  return column_sums

def make_backward_rows(forward_rows: List[int]) -> List[int]:
  """
  往路で取る行のリストから、復路で取る行のリストを作成する関数
  復路で取る行は、forward_rows内の行以外かつN-1行目以外の行をすべて含む
  N-1行目は含まない
  Args:
    forward_rows: 往路で取る行のリスト
  Returns:
    復路で取る行のリスト
  """
  backward_rows = []
  for i in range(N - 1):  # N-1行目は含まない
    if i not in forward_rows:
      backward_rows.append(i)
  return backward_rows


# 往路で取る行が正しいかを検証する関数
def validate_forward_rows(grid: List[List[int]], forward_rows: List[int], backward_rows: List[int]) -> bool:
  """
  往路で取る行が正しいかを検証する関数
  - forward_rows内のすべての行が、forward_rows内のいずれかの行と隣接しているか
  - N-2行目が必ずforward_rows内に含まれているか
  - backward_rows内のすべての行が、backward_rows内のいずれかの行と隣接しているか
    - ただし、0行目は隣接していなくてもよい
  Args:
    grid: 2次元リストで表されるグリッド
    forward_rows: 往路で取る行のリスト
    backward_rows: 復路で取る行のリスト
  Returns:
    往路で取る行が正しい場合はTrue、そうでない場合はFalse
  """

  # ソートされているはずだが、念のためソートしておく
  forward_rows.sort()
  backward_rows.sort()

  # forward_rows内のすべての行が、forward_rows内のいずれかの行と隣接しているか
  for i in range(len(forward_rows)):
    flag = False
    if i > 0 and forward_rows[i] - forward_rows[i - 1] == 1:
      flag = True
    if i < len(forward_rows) - 1 and forward_rows[i + 1] - forward_rows[i] == 1:
      flag = True
    if not flag:
      return False
    
  # N-2行目が必ずforward_rows内に含まれているか
  if N - 2 not in forward_rows:
    return False
  
  # backward_rows内のすべての行が、backward_rows内のいずれかの行と隣接しているか
  for i in range(len(backward_rows)):
    flag = False
    if backward_rows[i] == 0:  # 0行目は隣接していなくてもよい
      flag = True
    if i > 0 and backward_rows[i] - backward_rows[i - 1] == 1:
      flag = True
    if i < len(backward_rows) - 1 and backward_rows[i + 1] - backward_rows[i] == 1:
      flag = True
    if not flag:
      return False
  return True

# スコアを計算する関数
def calculate_score(column_sums: List[int], forward_rows: List[int], backward_rows: List[int]) -> int:
  """
  スコアを計算する関数
  往路で取る行のリストと復路で取る行のリストをもとに、スコアを計算する
  Args:
    column_sums: 列ごとの合計を格納したリスト
    forward_rows: 往路で取る行のリスト
    backward_rows: 復路で取る行のリスト
  Returns:
    スコア
  """

  reverced_backward_rows = backward_rows[::-1]  # 復路で取る行のリストを逆順にする

  score = 0
  count = (N-2)//2 # 行の中間の位置を基準に、スコアを近似する

  # 往路で取る行のスコアを計算する
  for row_idx in forward_rows:
    score += column_sums[row_idx] * count
    count += N//2
  count += N  # N-1行目の移動をカウント
  # 復路で取る行のスコアを計算する
  for row_idx in reverced_backward_rows:
    score += column_sums[row_idx] * count
    count += N//2

  return score

# ジグザグに移動する関数
def zigzag_move(start_x: int, start_y: int, end_x: int, end_y: int) -> List[Tuple[int, int]]:
  """
  ジグザグに移動する関数
  開始地点と終了地点を指定すると、ジグザグに移動するルートを返す
  Args:
    start_x: 開始地点のx座標
    start_y: 開始地点のy座標
    end_x: 終了地点のx座標
    end_y: 終了地点のy座標
  Returns:
    ジグザグに移動するルートを表すタプルのリスト
  """
  route = []
  current_x, current_y = start_x, start_y
  # route.append((current_x, current_y))

  while current_x != end_x or current_y != end_y:
    if current_x == start_x:
      current_x = end_x
    else:
      current_x = start_x

    route.append((current_x, current_y))
    if len(route) >= 2 and route[-1] == route[-2]:  # 直前の位置と同じ場合は、その移動をスキップする
      route.pop()

    if current_y < end_y:
      current_y += 1
    elif current_y > end_y:
      current_y -= 1

    route.append((current_x, current_y))
    if len(route) >= 2 and route[-1] == route[-2]:  # 直前の位置と同じ場合は、その移動をスキップする
      route.pop()

  return route

# 直線的に移動する関数
def straight_move(start_x: int, start_y: int, end_x: int, end_y: int) -> List[Tuple[int, int]]:
  """  直線的に移動する関数
  開始地点と終了地点を指定すると、直線的に移動するルートを返す
  Args:    start_x: 開始地点のx座標
    start_y: 開始地点のy座標
    end_x: 終了地点のx座標
    end_y: 終了地点のy座標
  Returns:    直線的に移動するルートを表すタプルのリスト
  """
  route = []
  current_x, current_y = start_x, start_y
  # route.append((current_x, current_y))

  while current_x != end_x:
    if current_x < end_x:
      current_x += 1
    else:
      current_x -= 1
    route.append((current_x, current_y))

  while current_y != end_y:
    if current_y < end_y:
      current_y += 1
    else:
      current_y -= 1
    route.append((current_x, current_y))

  return route

# ルートを構築する関数
def construct_route(forward_rows: List[int], backward_rows: List[int]) -> List[Tuple[int, int]]:
  """
  ルートを構築する関数
  往路で取る行のリストと復路で取る行のリストをもとに、ルートを構築する
  開始地点は(0, 0)
  往路では、N-1列目を通ることはできない
  復路では、0列目を通ることはできない
  往路は飛ばした行でも0列目は通らなければならない
  復路は飛ばした行でもN-1列目は通らなければならない
  連続して隣接する行の数が奇数ならば、最初の往路はジグザグに移動し、復路は直線的に移動する
  連続して隣接する行の数が偶数ならば、すべての移動は直線的に移動する
  往路と復路の間で、N-1行目を移動する
  Args:
    forward_rows: 往路で取る行のリスト
    backward_rows: 復路で取る行のリスト
  Returns:
    ルートを表すタプルのリスト
  """
  
  route = []
  current_x, current_y = 0, 0
  route.append((current_x, current_y))
  reversed_backward_rows = backward_rows[::-1]  # 復路で取る行のリストを逆順にする

  # 往路を、連続した要素ごとに分割する
  forward_segments = []
  current_segment = [forward_rows[0]]
  for i in range(1, len(forward_rows)):
    if forward_rows[i] == forward_rows[i - 1] + 1:
      current_segment.append(forward_rows[i])
    else:
      forward_segments.append(current_segment)
      current_segment = [forward_rows[i]]
  forward_segments.append(current_segment)

  # 復路も、連続した要素ごとに分割する
  backward_segments = []
  current_segment = [reversed_backward_rows[0]]
  for i in range(1, len(reversed_backward_rows)):
    if reversed_backward_rows[i] == reversed_backward_rows[i - 1] - 1:
      current_segment.append(reversed_backward_rows[i])
    else:
      backward_segments.append(current_segment)
      current_segment = [reversed_backward_rows[i]]
  backward_segments.append(current_segment)

  # 往路のセグメントごとにルートを構築する
  for segment in forward_segments:
    # 現在の位置から、セグメントの最初の行まで移動する
    route.extend(straight_move(current_x, current_y, segment[0], 0))  # 直線的に移動する
    current_x, current_y = route[-1]  # 直線的な移動の最後の位置を現在位置とする

    row_idx = 0
    if len(segment) % 2 == 1:  # 連続して隣接する行の数が奇数の場合
      route.extend(zigzag_move(current_x, current_y, segment[1], N-2))  # ジグザグに移動する
      row_idx = 2
    else:  # 連続して隣接する行の数が偶数の場合
      route.extend(straight_move(current_x, current_y, segment[0], N-2))  # 直線的に移動する
      row_idx = 1
    current_x, current_y = route[-1]  # 移動の最後の位置を現在位置とする

    for i in range(row_idx, len(segment)):
      if current_y == 0:
        route.extend(straight_move(current_x, current_y, segment[i], N-2))  # 直線的に移動する
      else:
        route.extend(straight_move(current_x, current_y, segment[i], 0))  # 直線的に移動する
      current_x, current_y = route[-1]  # 直線的な移動の最後の位置を現在位置とする

  # 往路と復路の間で、N-1行目を移動する
  route.extend(straight_move(current_x, current_y, N-1, N-1))  # 直線的に移動する
  current_x, current_y = route[-1]  # 直線的な移動の最後の位置を現在位置とする

  # 復路のセグメントごとにルートを構築する
  for segment in backward_segments:
    
    # 現在の位置から、セグメントの最初の行まで移動する
    route.extend(straight_move(current_x, current_y, segment[0], N-1))  # 直線的に移動する
    current_x, current_y = route[-1]  # 直線的な移動の最後の位置を現在位置とする

    row_idx = 0
    if len(segment) % 2 == 1 and len(segment) > 1:  # 連続して隣接する行の数が奇数の場合
      route.extend(zigzag_move(current_x, current_y, segment[1], 1))  # ジグザグに移動する
      row_idx = 2
    else:  # 連続して隣接する行の数が偶数の場合
      route.extend(straight_move(current_x, current_y, segment[0], 1))  # 直線的に移動する
      row_idx = 1
    current_x, current_y = route[-1]  # 移動の最後の位置を現在位置とする

    for i in range(row_idx, len(segment)):
      if current_y == N-1:
        route.extend(straight_move(current_x, current_y, segment[i], 1))  # 直線的に移動する
      else:
        route.extend(straight_move(current_x, current_y, segment[i], N-1))  # 直線的に移動する
      current_x, current_y = route[-1]  # 直線的な移動の最後の位置を現在位置とする

  if current_x != 0:  # 最後に、現在位置から0行目まで移動する
    route.extend(straight_move(current_x, current_y, 0, current_y))  # 直線的に移動する
    current_x, current_y = route[-1]  # 直線的な移動の最後の位置を現在位置とする

  return route

def main():
  _ = int(input())  # Nは200で固定されているため、入力は無視する
  grid = [list(map(int, input().split())) for _ in range(N)]

  column_sums = calculate_column_sums(grid)
  ic(column_sums)

  average_column_sum = sum(column_sums) / len(column_sums)
  ic(average_column_sum)

  # 往路で取る行のリスト
  forward_rows = list(range(N - 1))  # 最初の段階では、0行目からN-2行目まで全てを往路で取ることにする
  backward_rows = make_backward_rows(forward_rows)
  ic(backward_rows)

  best_forward_rows = forward_rows[:]  # 最良の往路で取る行のリスト
  best_score = -1  # 実際のスコアではなく、スコアの比較に使用する近似値

  roop_count = 0

  # 往路で取る行を山登りで決定する
  while time.time() - start_time < TIME_LIMIT:
    roop_count += 1
    # 往路で取る行のリストをランダムに変更する
    new_forward_rows = best_forward_rows[:]
    if random.random() < 0.5 and len(new_forward_rows) > 1:
      # 連続する2行を選択し、それぞれについて、往路にあれば削除する
      row_num = random.randint(0, len(new_forward_rows) - 4)  # 後で行を追加するため、最後の3行は除外
      if row_num in new_forward_rows:
        new_forward_rows.remove(row_num)
      if row_num + 1 in new_forward_rows:
        new_forward_rows.remove(row_num + 1)
    else:
      # 連続する2行を選択し、それぞれについて、往路になければ追加する
      row_num = random.randint(0, len(new_forward_rows) - 4)  # 後で行を追加するため、最後の3行は除外
      if row_num not in new_forward_rows:
        new_forward_rows.append(row_num)
      if row_num + 1 not in new_forward_rows:
        new_forward_rows.append(row_num + 1)
    new_forward_rows.sort()
    new_backward_rows = make_backward_rows(new_forward_rows)

    # 往路で取る行が正しいかを検証する
    if not validate_forward_rows(grid, new_forward_rows, new_backward_rows):
      continue

    # スコアを計算する
    new_score = calculate_score(column_sums, new_forward_rows, new_backward_rows)

    # より良いスコアを見つけた場合、更新する
    if new_score > best_score:
      best_score = new_score
      best_forward_rows = new_forward_rows[:]
      ic(best_score)

  route = construct_route(best_forward_rows, make_backward_rows(best_forward_rows))

  ic(len(route))

  # 結果を出力する
  for x, y in route[:40000]:
    print(x, y)

  ic(roop_count)

if __name__ == "__main__":
  main()