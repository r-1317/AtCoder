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

DIRS = ["D", "U", "R", "L"]

DIR_DICT = {
  "D": (1, 0),
  "U": (-1, 0),
  "R": (0, 1),
  "L": (0, -1)
}

RADIUS_LIMIT = 24**2  # 中心からの距離の二乗が一定以内のマスでのみ魔法陣の使用を許可する

BEAM_WIDTH = 10  # ビームサーチの幅

class State:
  def __init__(self, pos: List[int], circles: List[List[int]], moves: List[str | int], parent: "State" = None):
    self.pos = pos
    self.circles = circles
    self.moves = moves
    self.parent = parent

# 魔法陣を使うと、操作前の高橋くんの位置を (i, j)、選んだマスの座標を (a, b) として、高橋くんを (2a−i, 2b−j) へ移す。盤面外への移動はできない。
# 魔法陣を使った場合、操作前の座標(i, j)が新たな魔法陣の座標となる。

def manhattan_distance(pos1: List[int], pos2: List[int]) -> int:
  return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def eauclidean_distance_squared(pos1: List[int], pos2: List[int]) -> int:
  return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2

def get_all_moves_06(N: int, K: int, current_pos: List[int], current_goal_pos: List[int], circles: List[List[int]]) -> Tuple[List[str | int], List[int]]:
  moves = []
  new_positions = []

  # 魔法陣を使わない場合の移動
  for dir in DIRS:
    dx, dy = DIR_DICT[dir]
    new_pos = [current_pos[0] + dx, current_pos[1] + dy]
    if 0 <= new_pos[0] < N and 0 <= new_pos[1] < N:
      moves.append([dir])
      new_positions.append(new_pos)

  # 魔法陣を使う場合の移動
  for i, circle in enumerate(circles):
    if eauclidean_distance_squared(current_pos, [64, 64]) > RADIUS_LIMIT:
      break  # 魔法陣の使用は現在の座標が中心からの距離がRADIUS_LIMIT以内のマスでのみ許可される
    a, b = circle
    new_pos = [2 * a - current_pos[0], 2 * b - current_pos[1]]
    if 0 <= new_pos[0] < N and 0 <= new_pos[1] < N:
      moves.append(["J", a, b, i])  # 魔法陣の座標とインデックスを記録
      new_positions.append(new_pos)

  return moves, new_positions

def main():
  N, M, K, T = map(int, input().split())  # 盤面の大きさ(128固定)、目的地の数(150固定)、魔法陣の数(3固定)、移動可能な回数
  start = list(map(int, input().split()))  # スタート地点 (x, y)
  goals = [list(map(int, input().split())) for _ in range(M)]  # 目的地の座標 [(x, y), ...]

  circles = [[63, 63], [63, 64], [64, 63]]  # 魔法陣の座標 [(x, y), ...]
  current_pos = start
  current_goal_index = 0
  current_goal_pos = goals[current_goal_index]
  ans_list = []  # 移動の記録を保持する2次元リスト。U, D, L, R 及び魔法陣の使用を記録する。

  # 魔法陣の座標を先に出力する
  for circle in circles:
      print(*circle)

  # 目的地ごとにビームサーチで移動を決定する
  for goal_index in range(M):
    current_goal_pos = goals[goal_index]
    beam = [State(current_pos, circles, [])]  # ビームの初期状態

    while True:  # 目的地に到達するまでループ
      new_beam = []
      for state in beam:
        moves, new_positions = get_all_moves_06(N, K, state.pos, current_goal_pos, state.circles)
        for best_move, best_new_pos in zip(moves, new_positions):
          # 魔法陣を使った場合は、その座標を更新する
          if len(best_move) == 4:  # 魔法陣を使った場合
            _, a, b, circle_index = best_move
            new_circles = [circle[:] for circle in state.circles]
            new_circles[circle_index] = [state.pos[0], state.pos[1]]  # 魔法陣の座標を更新
            new_state = State(best_new_pos, new_circles, best_move[:3], state)
          else:
            new_state = State(best_new_pos, state.circles, best_move[:3], state)
          new_beam.append(new_state)
          # new_state = State(best_new_pos, best_move[:3], state)
        # new_beam.append(new_state)

      # ビーム幅を制限する
      new_beam.sort(key=lambda s: manhattan_distance(s.pos, current_goal_pos) + eauclidean_distance_squared(s.pos, [64, 64]) / 1000000)  # ゴールに近い順にソート
      beam = new_beam[:BEAM_WIDTH]

      # 目的地に到達した場合はループを終了
      if beam and beam[0].pos == current_goal_pos:
        break

    # 最終的にゴールに最も近い状態を選択する
    best_final_state = min(beam, key=lambda s: manhattan_distance(s.pos, current_goal_pos) + eauclidean_distance_squared(s.pos, [64, 64]) / 1000000)

    # 移動を遡って記録する
    moves = []
    state = best_final_state
    while state.parent is not None:
      moves.append(state.moves)
      state = state.parent
    moves.reverse()  # 移動の順序を逆にする(もとに戻す)
    ans_list.extend(moves)  # 移動の記録を保持する

    current_pos = best_final_state.pos  # 現在の位置を更新
    circles = best_final_state.circles  # 魔法陣の座標を更新

  # 出力
  for move in ans_list:
    print(*move)  # 移動の記録を出力

  score = M + T - len(ans_list) + 1
  ic(score)

if __name__ == "__main__":
  main()