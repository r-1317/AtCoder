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

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def main():
  N, M, K, T = map(int, input().split())  # 盤面の大きさ(128固定)、目的地の数(150固定)、魔法陣の数(3固定)、移動可能な回数
  start = list(map(int, input().split()))  # スタート地点 (x, y)
  goals = [list(map(int, input().split())) for _ in range(M)]  # 目的地の座標 [(x, y), ...]

  current_pos = start
  current_goal_index = 0
  current_goal_pos = goals[current_goal_index]
  ans_list = []  # 移動の記録を保持する2次元リスト。U, D, L, R 及び魔法陣の使用を記録する。

  for i in range(M):
    # 目的地に到達するまで移動
    while current_pos != current_goal_pos:
      if current_pos[0] < current_goal_pos[0]:
        ans_list.append(("D"))  # 下に移動
        current_pos[0] += 1
      elif current_pos[0] > current_goal_pos[0]:
        ans_list.append(("U"))  # 上に移動
        current_pos[0] -= 1
      elif current_pos[1] < current_goal_pos[1]:
        ans_list.append(("R"))  # 右に移動
        current_pos[1] += 1
      elif current_pos[1] > current_goal_pos[1]:
        ans_list.append(("L"))  # 左に移動
        current_pos[1] -= 1

    # 次の目的地に進む
    current_goal_index += 1
    if current_goal_index < M:
      current_goal_pos = goals[current_goal_index]

  # 出力
  for _ in range(K):
    print(0, 0)  # 魔法陣はすべて原点においておく

  for move in ans_list:
    print(*move)

  score = M + T - len(ans_list) + 1
  ic(score)

if __name__ == "__main__":
  main()