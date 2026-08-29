import os
from typing import Tuple, List
import time
import math

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

START_TIME = time.time()

TIME_LIMIT = 1.9
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # 右、下、左、上
N = 100  # 固定
M = 3  # 固定

# NxNの盤面を表現するビットボード
# https://github.com/r-1317/AtCoder/blob/main/library.py 
# Codonの64bit整数で使えるように改変
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


class Action:
  def __init__(self, m: int):
    self.m = m

class State:
  def __init__(self, turn: int,action: Action, danger_level: int, board: BitBoard):
    self.action = action
    self.tree_index = -1  # ChokudaiSearchPathNodeのインデックスを保持するための属性
    self.turn = turn  # 現在のターンを保持するための属性
    self.danger_level = danger_level  # 評価値を保持するための属性
    self.board = board  # ビットボードを保持するための属性

def time_check():
  return time.time() - START_TIME < TIME_LIMIT

def state_less(lhs: State, rhs: State) -> bool:
  return lhs.danger_level < rhs.danger_level

def nearest_distance(board: BitBoard, x: int, y: int) -> int:
  """
  board上の(x, y)から最も近い1の座標までのマンハッタン距離を返す。
  ここでは、盤面はトーラス状ではないので、端から端への移動は考慮しない。
  """
  min_distance = 10**9
  queue = [(x, y)]
  visited_bb = BitBoard(board.N)
  if board.is_set(x, y):
    return 0
  visited_bb.set(x, y)
  while queue:
    new_queue = []
    for cx, cy in queue:
      for dx, dy in DIRS:
        nx, ny = cx + dx, cy + dy
        if 0 <= nx < board.N and 0 <= ny < board.N:
          if not visited_bb.is_set(nx, ny):
            if board.is_set(nx, ny):
              return abs(nx - x) + abs(ny - y)
            visited_bb.set(nx, ny)
            new_queue.append((nx, ny))
    queue = new_queue
  return min_distance

MOVES = [(7, 1), (7, 1), (29, 37)]  # 今は雑に決めた

def get_next_states(state: State, hunting_list: List[Tuple[int, int]]) -> List[State]:
  """
  現在の状態から次の状態を生成する関数。
  MOVESの中から1つ選び、それだけ移動する。トーラス状の盤面なので、移動後の座標はNで割った余りを取る。
  移動した先にお札を置き、BitBoardのその座標を1にする。
  置き終わると、hunting_listの現在のターンに対応する座標に怪異が発生するので、danger_levelを以下の式で更新する。
  danger_level += ((距離) * math.floor(math.sqrt(turn + 1)))  ただし、距離は最も近いお札と怪異の座標のマンハッタン距離。
  ### 入力
  - state: 現在の状態
  - hunting_list: ターンごとの怪異の座標リスト
  ### 出力
  - 次の状態のリスト
  """
  next_states = []
  for i, move in enumerate(MOVES):
    new_x = (state.action.m + move[0]) % N
    new_y = (state.action.m + move[1]) % N
    new_board = BitBoard(N, state.board.board[:])  # 現在のビットボードをコピー
    new_board.set(new_x, new_y)
    turn = state.turn + 1
    if turn < len(hunting_list):
      hunting_x, hunting_y = hunting_list[turn]
      distance = nearest_distance(new_board, hunting_x, hunting_y)
      danger_level = state.danger_level + (distance * math.floor(math.sqrt(turn + 1)))
    else:
      danger_level = state.danger_level
    next_states.append(State(turn=turn, action=Action(m=i), danger_level=danger_level, board=new_board))
  return next_states


# (ここから) https://github.com/r-1317/2026_sotsuken_programs/blob/master/structs/chokudai_search.py
class _Entry[State]:
    state: State
    order: int

    def __init__(self, state: State, order: int):
        self.state = state
        self.order = order


def _entry_before(lhs, rhs, state_less):
    if state_less(lhs.state, rhs.state):
        return True
    if state_less(rhs.state, lhs.state):
        return False
    # 同評価値は生成が早い状態を優先する。
    return lhs.order < rhs.order


def _check_constructor_arguments(search_depth, r):
    if search_depth < 0:
        raise ValueError("search_depth must be non-negative")
    if r <= 0:
        raise ValueError("r must be positive")


def _check_level(level, search_depth):
    if level < 0 or level > search_depth:
        raise IndexError("level is outside the search depth")

RED = True
BLACK = False


class _RBNode[State]:
    entry: _Entry[State]
    left: int
    right: int
    red: bool

    def __init__(self, entry: _Entry[State], red: bool):
        self.entry = entry
        self.left = -1
        self.right = -1
        self.red = red

# left-leaning red-black tree。この探索で必要な挿入、最良の取得、
# 最悪の削除だけを実装する。
class _RBLevel[State, StateLess]:
    nodes: list[_RBNode[State]]
    free_nodes: list[int]
    state_less: StateLess
    root: int
    node_count: int

    def __init__(self, state_less: StateLess):
        self.nodes = []
        self.free_nodes = []
        self.root = -1
        self.node_count = 0
        self.state_less = state_less

    def __len__(self):
        return self.node_count

    def empty(self):
        return self.node_count == 0

    def _new_node(self, entry: _Entry[State]):
        if len(self.free_nodes) > 0:
            index = self.free_nodes.pop()
            self.nodes[index] = _RBNode(entry, RED)
            return index
        self.nodes.append(_RBNode(entry, RED))
        return len(self.nodes) - 1

    def _release_node(self, index):
        self.free_nodes.append(index)

    def _is_red(self, index):
        return index >= 0 and self.nodes[index].red == RED

    def _rotate_left(self, index):
        node = self.nodes[index]
        new_root_index = node.right
        new_root = self.nodes[new_root_index]
        node.right = new_root.left
        new_root.left = index
        new_root.red = node.red
        node.red = RED
        return new_root_index

    def _rotate_right(self, index):
        node = self.nodes[index]
        new_root_index = node.left
        new_root = self.nodes[new_root_index]
        node.left = new_root.right
        new_root.right = index
        new_root.red = node.red
        node.red = RED
        return new_root_index

    def _flip_colors(self, index):
        node = self.nodes[index]
        node.red = not node.red
        if node.left >= 0:
            self.nodes[node.left].red = not self.nodes[node.left].red
        if node.right >= 0:
            self.nodes[node.right].red = not self.nodes[node.right].red

    def _insert(self, index, entry):
        if index < 0:
            return self._new_node(entry)

        node = self.nodes[index]
        if _entry_before(entry, node.entry, self.state_less):
            node.left = self._insert(node.left, entry)
        else:
            node.right = self._insert(node.right, entry)

        if self._is_red(node.right) and not self._is_red(node.left):
            index = self._rotate_left(index)
            node = self.nodes[index]
        if self._is_red(node.left) and self._is_red(self.nodes[node.left].left):
            index = self._rotate_right(index)
            node = self.nodes[index]
        if self._is_red(node.left) and self._is_red(node.right):
            self._flip_colors(index)
        return index

    def add(self, entry: _Entry[State]):
        self.root = self._insert(self.root, entry)
        self.nodes[self.root].red = BLACK
        self.node_count += 1

    def _move_red_left(self, index):
        self._flip_colors(index)
        node = self.nodes[index]
        if node.right >= 0 and self._is_red(self.nodes[node.right].left):
            node.right = self._rotate_right(node.right)
            index = self._rotate_left(index)
            self._flip_colors(index)
        return index

    def _move_red_right(self, index):
        self._flip_colors(index)
        node = self.nodes[index]
        if node.left >= 0 and self._is_red(self.nodes[node.left].left):
            index = self._rotate_right(index)
            self._flip_colors(index)
        return index

    def _fix_up(self, index):
        node = self.nodes[index]
        if self._is_red(node.right):
            index = self._rotate_left(index)
            node = self.nodes[index]
        if self._is_red(node.left) and self._is_red(self.nodes[node.left].left):
            index = self._rotate_right(index)
            node = self.nodes[index]
        if self._is_red(node.left) and self._is_red(node.right):
            self._flip_colors(index)
        return index

    def _delete_min(self, index):
        node = self.nodes[index]
        if node.left < 0:
            self._release_node(index)
            return -1
        if not self._is_red(node.left) and not self._is_red(
            self.nodes[node.left].left
        ):
            index = self._move_red_left(index)
            node = self.nodes[index]
        node.left = self._delete_min(node.left)
        return self._fix_up(index)

    def _delete_max(self, index):
        node = self.nodes[index]
        if self._is_red(node.left):
            index = self._rotate_right(index)
            node = self.nodes[index]
        if node.right < 0:
            self._release_node(index)
            return -1
        if not self._is_red(node.right) and not self._is_red(
            self.nodes[node.right].left
        ):
            index = self._move_red_right(index)
            node = self.nodes[index]
        node.right = self._delete_max(node.right)
        return self._fix_up(index)

    def pop_best(self):
        if self.root < 0:
            raise IndexError("pop from an empty red-black tree")
        best_index = self.root
        while self.nodes[best_index].left >= 0:
            best_index = self.nodes[best_index].left
        result = self.nodes[best_index].entry.state

        root_node = self.nodes[self.root]
        if not self._is_red(root_node.left) and not self._is_red(root_node.right):
            root_node.red = RED
        self.root = self._delete_min(self.root)
        if self.root >= 0:
            self.nodes[self.root].red = BLACK
        self.node_count -= 1
        return result

    def remove_worst(self):
        if self.root < 0:
            return
        root_node = self.nodes[self.root]
        if not self._is_red(root_node.left) and not self._is_red(root_node.right):
            root_node.red = RED
        self.root = self._delete_max(self.root)
        if self.root >= 0:
            self.nodes[self.root].red = BLACK
        self.node_count -= 1


# 各層を赤黒木で管理し、最良 r 個だけを保持する。
class RBTreeStates[State, StateLess]:
    levels: list[_RBLevel[State, StateLess]]
    search_depth: int
    r: int
    next_order: int

    def __init__(self, search_depth: int, r: int, state_less: StateLess):
        _check_constructor_arguments(search_depth, r)
        self.search_depth = search_depth
        self.r = r
        self.levels = [_RBLevel(state_less) for _ in range(search_depth + 1)]
        self.next_order = 0

    def add(self, level: int, state: State):
        _check_level(level, self.search_depth)
        tree = self.levels[level]
        tree.add(_Entry(state, self.next_order))
        self.next_order += 1
        if len(tree) > self.r:
            tree.remove_worst()

    def pop(self, level):
        _check_level(level, self.search_depth)
        return self.levels[level].pop_best()

    def empty(self, level):
        _check_level(level, self.search_depth)
        return self.levels[level].empty()

    def size(self, level):
        _check_level(level, self.search_depth)
        return len(self.levels[level])


class ChokudaiSearchPathNode[Action]:
    parent: int
    action: Action

    def __init__(self, parent: int, action: Action):
        self.parent = parent
        self.action = action


def get_path(tree, tree_index):
    path = []
    while tree_index >= 0:
        node = tree[tree_index]
        path.append(node.action)
        tree_index = node.parent
    path.reverse()
    return path


# 問題ごとに次の3関数を実装する必要がある。
#
#   def state_less(lhs, rhs): ...
#   def get_next_states(state): ...
#   def time_check(): ...
#
# デフォルトは研究の提案法 AVLTreeStates。_chokudai_search 内の
# AVLTreeStates を HeapStates または RBTreeStates に置き換えるだけで比較できる。
def _chokudai_search(
    first_state,
    search_depth,
    chokudai_width,
    max_loop,
    state_less_function,
    get_next_states_function,
    time_check_function,
    hunting_list
):
    if chokudai_width <= 0:
        raise ValueError("chokudai_width must be positive")
    if max_loop <= 0:
        raise ValueError("max_loop must be positive")

    if search_depth < 0:
        raise ValueError("search_depth must be non-negative")

    # 1層から今後取り出し得る最大数。この個数まで保持すれば、
    # それより悪い状態は従来法でも取り出されない。
    state_limit = chokudai_width * max_loop
    states = RBTreeStates(search_depth, state_limit, state_less_function)
    path_tree = []

    # 初期状態には直前の操作がないため、木の外側を指す。
    first_state.tree_index = -1
    states.add(0, first_state)

    for _ in range(max_loop):
        if not time_check_function():
            break

        for depth in range(search_depth):
            for _ in range(chokudai_width):
                if states.empty(depth):
                    break
                current = states.pop(depth)

                for next_state in get_next_states_function(current, hunting_list):
                    next_tree_index = len(path_tree)
                    path_tree.append(
                        ChokudaiSearchPathNode(
                            current.tree_index, next_state.action
                        )
                    )
                    next_state.tree_index = next_tree_index
                    states.add(depth + 1, next_state)

    # 原則として最終層を選ぶ。行き止まりのある問題で最終層が
    # 空の場合は、参考実装と同様に最も深い非空層から選ぶ。
    for depth in range(search_depth, -1, -1):
        if not states.empty(depth):
            best = states.pop(depth)
            return get_path(path_tree, best.tree_index)

    return []

def chokudai_search(first_state, search_depth, chokudai_width, max_loop, hunting_list):
    return _chokudai_search(
        first_state,
        search_depth,
        chokudai_width,
        max_loop,
        state_less,  # 問題ごとに実装する必要がある。
        get_next_states,  # 問題ごとに実装する必要がある。
        time_check,  # 問題ごとに実装する必要がある。
        hunting_list
    )
# (ここまで) https://github.com/r-1317/2026_sotsuken_programs/blob/master/structs/chokudai_search.py

def main():
  _N, _M = map(int, input().split())  # 受け取るだけで、使用はしない
  haunting_list = [tuple(map(int, input().split())) for _ in range(N)]  # ターンiで怪異が発生する座標(x, y)のリスト

  first_state = State(turn=-1, action=Action(m=-1), danger_level=0.0, board=BitBoard(N))
  result = chokudai_search(first_state, search_depth=10000, chokudai_width=1, max_loop=10000, hunting_list=haunting_list)

  # ic(result)
  for row in MOVES:
    print(row[0], row[1])
  for action in result:
    print(action.m)

if __name__ == "__main__":
  main()