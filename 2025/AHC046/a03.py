# a03.py  ―  AHC046  simple solver (obstacle trick + BFS shortest path)
import os
from collections import deque
from typing import List, Tuple

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
    from icecream import ic
    ic.disable()
else:
    def ic(*args):  # type: ignore
        return None

ic.enable() if MyPC else None
# ----------------------------------------------------------------------

DIRS = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]   # (di,dj,char)

# move_by_step: (現在の座標, 次の座標) -> (移動方向, 移動先の座標)
def move_by_step(current_coord: list[int, int], next_coord: list[int, int]) -> Tuple[Tuple[str, str], list[int, int]]:
  # x軸正の方向に移動する
  if current_coord[0] < next_coord[0]:
    current_coord[0] += 1
    return ("M", "D"), current_coord
  
  # x軸負の方向に移動する
  elif current_coord[0] > next_coord[0]:
    current_coord[0] -= 1
    return ("M", "U"), current_coord
  
  # y軸正の方向に移動する
  elif current_coord[1] < next_coord[1]:
    current_coord[1] += 1
    return ("M", "R"), current_coord
  
  # y軸負の方向に移動する
  elif current_coord[1] > next_coord[1]:
    current_coord[1] -= 1
    return ("M", "L"), current_coord

  # 現在の座標と次の座標が同じ場合はエラーを返す
  else:
    ic(current_coord, next_coord)
    raise ValueError("Current coordinate and next coordinate are the same")

# move: (現在の座標, 次の座標) -> (移動方向, 移動先の座標)
def move(current_coord: list[int, int], next_coord: list[int, int]) -> Tuple[Tuple[str, str], list[int, int]]:
  # 1歩ずつ移動した場合と、x軸またはy軸の正または負の方向に滑走した場合のコストを計算する
  # 1歩ずつ移動した場合(マンハッタン距離)
  step_cost = abs(current_coord[0] - next_coord[0]) + abs(current_coord[1] - next_coord[1])
  # x軸正の方向に滑走した場合
  skate_D_cost = abs(n - next_coord[0]) + abs(current_coord[1] - next_coord[1]) + 1  # 滑走するため+1
  # x軸負の方向に滑走した場合
  skate_U_cost = abs(1 - next_coord[0]) + abs(current_coord[1] - next_coord[1]) + 1  # 滑走するため+1
  # y軸正の方向に滑走した場合
  skate_R_cost = abs(current_coord[0] - next_coord[0]) + abs(n - next_coord[1]) + 1  # 滑走するため+1
  # y軸負の方向に滑走した場合
  skate_L_cost = abs(current_coord[0] - next_coord[0]) + abs(1 - next_coord[1]) + 1  # 滑走するため+1
  
  # 1歩ずつ移動した場合と、滑走した場合のコストを比較する
  min_cost = min(step_cost, skate_D_cost, skate_U_cost, skate_R_cost, skate_L_cost)
  # 最小コストの動きを選択する
  if min_cost == skate_D_cost:
    # x軸正の方向に滑走する
    current_coord[0] = n
    return ("S", "D"), current_coord
  elif min_cost == skate_U_cost:
    # x軸負の方向に滑走する
    current_coord[0] = 1
    return ("S", "U"), current_coord
  elif min_cost == skate_R_cost:
    # y軸正の方向に滑走する
    current_coord[1] = n
    return ("S", "R"), current_coord
  elif min_cost == skate_L_cost:
    # y軸負の方向に滑走する
    current_coord[1] = 1
    return ("S", "L"), current_coord
  else:
    # 1歩ずつ移動する
    return move_by_step(current_coord, next_coord)


def main02(coord_list):
  # global n
  # global m
  # n, m = map(int, input().split())
  # coord_list = [list(map(int, input().split())) for _ in range(m)]

  grid = [[0] * (n+2) for _ in range(n+2)]  # 0なら空きマス、1なら障害物
  # 周囲のマスを障害物にする
  for i in range(n+2):
    grid[i][0] = grid[i][n+1] = 1
  for j in range(n+2):
    grid[0][j] = grid[n+1][j] = 1

  # 座標をすべて+1する
  coord_list = [[x+1, y+1] for x, y in coord_list]

  current_coord = [coord_list[0][0], coord_list[0][1]]  # 現在の座標を初期化

  # 障害物を設置せず、滑走または1歩ずつ移動する
  ans_list = []
  # 1からm-1までの座標を順に移動する
  for i in range(1, m):
    next_coord = coord_list[i]
    # 目的地に到達するまで移動する
    while current_coord != next_coord:
      # ic(current_coord, next_coord)
      # next_moove, current_coord = move(current_coord, next_coord)
      retrun_val = move(current_coord, next_coord)
      # ic(retrun_val)
      next_moove, current_coord = retrun_val
      # try:
      #   next_moove, current_coord = retrun_val
      # except:
      #   ic(current_coord, next_coord)
      #   raise ValueError("Current coordinate and next coordinate are the same")
      ans_list.append(next_moove)

  # 回答を出力
  for ans in ans_list:
    print(*ans)



def move03(start: List[int],
           goal: List[int],
           grid: List[List[int]]) -> List[Tuple[str, str]]:
    """
    現在位置 start から goal まで、(行動, 方向) を最短手数で列挙して返す。
    行動は 'M' (1 マス移動) or 'S' (滑走)、方向は 'UDLR'。
    """
    if start == goal:         # 既に到達
        return []

    q = deque([tuple(start)])
    prev: dict[Tuple[int, int], Tuple[Tuple[int, int], str, str] | None] = {
        tuple(start): None}

    while q:
        i, j = q.popleft()

        # 1 マス移動候補
        for di, dj, dc in DIRS:
            ni, nj = i + di, j + dj
            if grid[ni][nj] == 0 and (ni, nj) not in prev:
                prev[(ni, nj)] = ((i, j), 'M', dc)
                q.append((ni, nj))

        # 滑走候補
        for di, dj, dc in DIRS:
            ni, nj = i, j
            while grid[ni + di][nj + dj] == 0:
                ni += di
                nj += dj
            if (ni, nj) != (i, j) and (ni, nj) not in prev:
                prev[(ni, nj)] = ((i, j), 'S', dc)
                q.append((ni, nj))

        if tuple(goal) in prev:        # 早期終了
            break

    if tuple(goal) not in prev:
        raise RuntimeError('goal is unreachable')

    # 経路を復元
    path: List[Tuple[str, str]] = []
    cur = tuple(goal)
    while prev[cur] is not None:
        par, act, dc = prev[cur]          # type: ignore
        path.append((act, dc))
        cur = par
    path.reverse()
    return path


# ----------------------------------------------------------------------
def main() -> None:
    global n
    global m
    n, m = map(int, input().split())
    targets = [list(map(int, input().split())) for _ in range(m)]

    # (9,9)または(10,0)に目的地がある場合、02に移行
    flag = False
    for i in range(m):
        if targets[i][0] == 9 and targets[i][1] == 9:
            flag = True
            break
        if targets[i][0] == 10 and targets[i][1] == 0:
            flag = True
            break
    if flag:
        ic("a02に移行")
        main02(targets)
        return

    # 1-based にシフトし、番兵を持つ (n+2)×(n+2) の盤面を作る
    targets = [[x + 1, y + 1] for x, y in targets]
    grid = [[1] * (n + 2)]
    for _ in range(n):
        grid.append([1] + [0] * n + [1])
    grid.append([1] * (n + 2))

    cur = targets[0][:]        # 現在位置 (= 初期位置)
    ans: List[Tuple[str, str]] = []

    # --- 障害物 2 個を置く定型プロローグ ---------------------------
    ans.extend(move03(cur, [10, 9], grid))
    cur = [10, 9]

    ans.append(('A', 'R'))      # (10,10) をトグル
    grid[10][10] = 1            # 立てる

    ans.extend(move03(cur, [10, 1], grid))
    cur = [10, 1]

    ans.append(('A', 'D'))      # (11,1) をトグル
    grid[11][1] = 1
    # -------------------------------------------------------------

    # 目的地を順に訪問
    for idx in range(1, m):
        nxt = targets[idx]
        ans.extend(move03(cur, nxt, grid))
        cur = nxt

    # 出力
    for act, dc in ans:
        print(act, dc)


# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
