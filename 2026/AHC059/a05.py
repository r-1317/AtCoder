import os
from typing import Tuple, List, Optional
from collections import deque
import sys
import time
import heapq

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 20  # グリッドのサイズ。20固定
TIME_LIMIT = 1.9  # 秒数制限
MAX_WIDTH = 1000  # chokudai_levelの最大幅

start_time = time.time()  # 開始時刻を記録

class IsUsedBB:
  """ ビットボードで使用済みマスを管理するクラス """
  def __init__(self):
    self.board = 0  # 20x20のビットボードを初期化

  def is_used(self, x: int, y: int) -> bool:
    return (self.board >> (x * N + y)) & 1 == 1

  def set_used(self, x: int, y: int):
    self.board |= (1 << (x * N + y))

  def copy(self) -> 'IsUsedBB':
    new_bb = IsUsedBB()
    new_bb.board = self.board  # intなのでそのままコピーでOK
    return new_bb

def is_valid_pos(x: int, y: int) -> bool:
  return 0 <= x < N and 0 <= y < N

def manhattan_dist(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
  """ マンハッタン距離を計算する """
  return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def nearest_valid(pos: Tuple[int, int], used: IsUsedBB) -> Tuple[int, int]:
  """ 最寄りの未使用マスを探す """
  x, y = pos
  min_dist = float("inf")

  # BFSで最寄りの未使用マスを探索
  queue = deque()
  queue.append((x, y, 0))  # (x座標, y座標, 距離)
  visited = [[False] * N for _ in range(N)]
  visited[x][y] = True
  directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  while queue:
    cx, cy, dist = queue.popleft()

    if not used.is_used(cx, cy):
      return (cx, cy)

    for dx, dy in directions:
      nx, ny = cx + dx, cy + dy
      if is_valid_pos(nx, ny) and not visited[nx][ny]:
        visited[nx][ny] = True
        queue.append((nx, ny, dist + 1))

  # 見つからなかった場合
  raise ValueError("No unused cell found")

def get_pair_pos(num: int, nums_idx_list: List[List[Tuple[int, int]]], other_pos: Tuple[int, int]) -> Tuple[int, int]:
  """
  numのもう一方の位置を返す
  入力:
    num: 対応する数字
    nums_idx_list: 各数字の位置を格納するリスト
    other_pos: 既に知っている位置
  出力:
    numのもう一方の位置
  """
  pos1, pos2 = nums_idx_list[num]
  return pos2 if pos1 == other_pos else pos1

def make_commands(collect_order: List[Tuple[int, int]], current_pos: Tuple[int, int]) -> List[str]:
  """
  収集順序に基づいてコマンド列を生成する
  入力:
    collect_order: 収集順序のリスト
    current_pos: 現在位置
  出力:
    コマンド列のリスト
  """

  commands = []
  x, y = current_pos

  for target in collect_order:
    tx, ty = target
    
    # 縦移動
    while x < tx:
      commands.append('D')
      x += 1
    while x > tx:
      commands.append('U')
      x -= 1
    # 横移動
    while y < ty:
      commands.append('R')
      y += 1
    while y > ty:
      commands.append('L')
      y -= 1
    commands.append('Z')  # 収集コマンド
    x, y = tx, ty

  return commands

def get_path_length(path: List[Tuple[int, int]]) -> int:
  """ 経路の長さを計算する """
  length = 0
  for i in range(1, len(path)):
    length += manhattan_dist(path[i-1], path[i])
  return length

def find_best_next_pos(
  collect_order: List[Tuple[int, int]],
  collect_stack: List[Tuple[int, int]],
  used: IsUsedBB,
  nums_idx_list: List[List[Tuple[int, int]]],
  grid: List[List[int]],
) -> Tuple[int, int]:
  """
  次に収集するマスを決定する
  colect_ordrerの末尾と今回選択するマスの距離 + collect_stackの末尾と今回選択するマスの対のマスの距離 が最小になるマスを選ぶ
  入力:
    collect_order: 収集順序のリスト
    collect_stack: 2つめの数字を回収する際の経路のスタック
    used: 使用済みマスの管理リスト
    nums_idx_list: 各数字の位置を格納するリスト
    grid: グリッドの数字配置
  出力:
    次に収集するマスの位置
  """
  min_total_dist = float("inf")
  best_pos: Optional[Tuple[int, int]] = None

  for i in range(N):
    for j in range(N):
      if used.is_used(i, j):
        continue
      candidate_pos = (i, j)
      num = grid[i][j]
      pair_pos = get_pair_pos(num, nums_idx_list, candidate_pos)
      dist_1 = manhattan_dist(collect_order[-1], candidate_pos) if collect_order else 0  # collect_orderが空の場合は0
      dist_2 = manhattan_dist(collect_stack[-1], pair_pos) if collect_stack else 0  # collect_stackが空の場合は0
      total_dist = dist_1 + dist_2
      if total_dist < min_total_dist:
        min_total_dist = total_dist
        best_pos = candidate_pos

  if best_pos is None:
    raise ValueError("No unused cell found")
  return best_pos

# chokudaiサーチのノード
class Node:
  def __init__(self, used: IsUsedBB, current_pos: Tuple[int, int], stack_top: Optional[Tuple[int, int]] = None, prev_path_length: int = 0, prev_node: Optional['Node'] = None):
    """
    入力:
      used: 使用済みマスのビットボード
      current_pos: 現在位置
      stack_top: スタックのトップにある座標 (デフォルトは None)
      prev_path_length: これまでの経路長 (デフォルトは 0)
      prev_node: 前のノード (デフォルトは None)
    出力:      なし
    """
    self.used = used
    self.current_pos = current_pos
    self.stack_top = stack_top
    self.prev_path_length = prev_path_length
    self.prev_node = prev_node

  def __lt__(self, other: 'Node') -> bool:
    """ ノードの比較関数 (経路長で比較) """
    return self.prev_path_length < other.prev_path_length

  def next_nodes(self, grid: List[List[int]], nums_idx_list: List[List[Tuple[int, int]]]) -> List['Node']:
    """
    次のノードのリストを生成する
    入力:
      grid: グリッドの数字配置
      nums_idx_list: 各数字の位置を格納するリスト
    出力:
      次のノードのリスト
    """
    next_nodes = []
    for i in range(N):
      for j in range(N):
        if self.used.is_used(i, j):
          continue
        candidate_pos = (i, j)
        num = grid[i][j]
        pair_pos = get_pair_pos(num, nums_idx_list, candidate_pos)

        # 新しい使用済みビットボードを作成
        new_used = self.used.copy()
        new_used.set_used(i, j)
        new_used.set_used(pair_pos[0], pair_pos[1])

        # 新しい経路長を計算
        dist_1 = manhattan_dist(self.current_pos, candidate_pos)
        dist_2 = manhattan_dist(self.stack_top, pair_pos) if self.stack_top else 0
        new_path_length = self.prev_path_length + dist_1 + dist_2

        # 新しいノードを作成
        new_node = Node(
          used=new_used,
          current_pos=candidate_pos,
          stack_top=pair_pos,
          prev_path_length=new_path_length,
          prev_node=self
        )
        next_nodes.append(new_node)

    return next_nodes
  
  def reconstruct_path(self) -> List[Tuple[int, int]]:
    """
    ノードから経路を再構築する
    入力:      なし
    出力:
      経路のリスト
    """
    path = []
    path_2 = []  # スタックの方の経路を一時的に保存するリスト
    node = self
    while node is not None:
      path.append(node.current_pos)
      if node.stack_top is not None:
        path_2.append(node.stack_top)
      node = node.prev_node
    # 最初の座標(0,0)は重複しているので削除
    first = path.pop()  # ここでは末尾が最初の座標になる
    if not (first == (0, 0)):  # 安全確認
      raise ValueError("The first position is not (0,0)")
    path.reverse()  # 順方向に直す
    path.extend(path_2)  # スタックの方は最初から順方向なのでそのまま追加
    return path
  
  def total_cost(self) -> int:
    """
    ノードの総コストを計算する
    今までの経路長 + 現在位置からstackのトップまでの距離
    入力:      なし
    出力:
      総コスト
    """
    return self.prev_path_length + manhattan_dist(self.current_pos, self.stack_top) if self.stack_top else self.prev_path_length  # stack_topがNoneのときにこれが実行されることはないはずだが、念のため

def main():
  _ = int(input())  # Nは20で固定なので無視

  grid = [list(map(int, input().split())) for _ in range(N)]

  nums_idx_list = [[] for _ in range(N**2)]  # 各数字の位置を格納するリスト (各数字が2つずつ存在する)
  for i in range(N):
    for j in range(N):
      num = grid[i][j]
      nums_idx_list[num].append((i, j))
  
  used = IsUsedBB()  # 使用済みマスの管理

  # collect_order: List[Tuple[int, int]] = []  # 収集順序を格納するリスト

  current_pos = (0, 0)  # 現在位置

  # collect_stack = []  # 2つめの数字を回収する際の経路のスタック

# chokudaiサーチで収集順序を決定
  root_node = Node(used=used, current_pos=current_pos)
  chokudai_levels: List[List[Node]] = [[] for _ in range(N**2//2 + 1)]  # 各レベルのノードリスト。レベルごとにheapとして管理
  chokudai_levels[0].append(root_node)

  # for i in range(N**2//2):
  #   next_beam_nodes = []
  #   for node in beam_nodes:
  #     next_nodes = node.next_nodes(grid, nums_idx_list)
  #     next_beam_nodes.extend(next_nodes)
  #   # 経路長でソートして上位K個を残す
  #   if i < N**2//2 - 1:  # 最後のステップ以外では経路長でソート
  #     next_beam_nodes.sort(key=lambda n: n.prev_path_length)
  #   else:  # 最後のステップでは総コストでソート
  #     next_beam_nodes.sort(key=lambda n: n.total_cost())
  #   beam_nodes = next_beam_nodes[:K]

  flag = True

  while flag:
    for i in range(N**2//2):
      chokudai_level = chokudai_levels[i]
      next_chokudai_level = chokudai_levels[i + 1]
      if not chokudai_level:  # ノードが空ならスキップ
        continue
      node = heapq.heappop(chokudai_level)
      next_nodes = node.next_nodes(grid, nums_idx_list)
      for next_node in next_nodes:
        heapq.heappush(next_chokudai_level, next_node)
      # chokudai_levelの最大幅を制限
      while len(next_chokudai_level) > MAX_WIDTH:
        next_chokudai_level.pop()  # コストの高いノードをリストの末尾から通常の削除
      # 時間制限チェック
      elapsed_time = time.time() - start_time
      if elapsed_time > TIME_LIMIT:
        flag = False
        break

  # 最終レベルで総コストでソート
  chokudai_levels[-1].sort(key=lambda n: n.total_cost())

  # 最良ノードを取得
  best_node = chokudai_levels[-1][0]
  collect_order = best_node.reconstruct_path()

  # 経路を出力
  commands = make_commands(collect_order, (0, 0))
  for cmd in commands:
    print(cmd)

  # 総コストの確認 (デバッグ用)
  total_length = get_path_length(collect_order)
  print(f"Total path length: {total_length}", file=sys.stderr)

if __name__ == "__main__":
  main()