import os

EMPTY = -1
DO_NOTHING = -1
STATION = 0
RAIL_HORIZONTAL = 1
RAIL_VERTICAL = 2
RAIL_LEFT_DOWN = 3
RAIL_LEFT_UP = 4
RAIL_RIGHT_UP = 5
RAIL_RIGHT_DOWN = 6
COST_STATION = 5000
COST_RAIL = 100
N = 50
T = 800
COSTS = (COST_STATION, COST_RAIL, COST_RAIL, COST_RAIL, COST_RAIL, COST_RAIL, COST_RAIL)

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# マンハッタン距離を求める
def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> list:
  return abs(x1 - x2) + abs(y1 - y2)

# 2点間の経路を求める
def get_path01(x1: int, y1: int, x2: int, y2: int) -> list:
  path = []
  # 開始地点に駅を設置
  path.append((STATION, x1, y1))
  # 終了地点に駅を設置
  path.append((STATION, x2, y2))
  # 2点間の経路に線路を敷設
  tmp_pos = [x1, y1]
  # x軸方向の向きを確認
  x_dir = 0
  if x1 < x2:
    x_dir = 1
  elif x2 < x1:
    x_dir = -1
  tmp_pos[0] += x_dir  # 開始地点の次の座標
  # y軸方向の向きを確認
  y_dir = 0
  if y1 < y2:
    y_dir = 1
  elif y2 < y1:
    y_dir = -1
  # x軸方向に線路を敷設
  while tmp_pos[0] != x2:
    path.append((RAIL_VERTICAL, tmp_pos[0], tmp_pos[1]))
    if x1 < x2:
      tmp_pos[0] += 1
    elif x2 < x1:
      tmp_pos[0] -= 1
  # 曲がり角を設置
  if x_dir == 1:
    if y_dir == 1:
      path.append((RAIL_RIGHT_UP, tmp_pos[0], tmp_pos[1]))
    elif y_dir == -1:
      path.append((RAIL_LEFT_UP, tmp_pos[0], tmp_pos[1]))
  elif x_dir == -1:
    if y_dir == 1:
      path.append((RAIL_RIGHT_DOWN, tmp_pos[0], tmp_pos[1]))
    elif y_dir == -1:
      path.append((RAIL_LEFT_DOWN, tmp_pos[0], tmp_pos[1]))
  tmp_pos[1] += y_dir  # 曲がり角の次の座標
  # y軸方向に線路を敷設
  while tmp_pos[1] != y2:
    path.append((RAIL_HORIZONTAL, tmp_pos[0], tmp_pos[1]))
    if y1 < y2:
      tmp_pos[1] += 1
    else:
      tmp_pos[1] -= 1

  return path

# 現在の資金で建てられる通勤経路の住民番号を列挙
def get_commuter_list(money: int, home_list: list, workplace_list: list) -> list:
  commuter_list = []
  for i in range(len(home_list)):
    xh, yh = home_list[i]
    xw, yw = workplace_list[i]
    # 通勤経路の建設コスを計算
    path_cost = COST_STATION * 2 + COST_RAIL * manhattan_distance(xh, yh, xw, yw)
    if path_cost <= money:
      commuter_list.append(i)

  return commuter_list

# 家同士・職場同士の距離が最も近い住民との距離が最も近い組を求める
def get_nearest_commuters(commuter_list: list, home_list: list, workplace_list: list) -> list:
  nearest_commuters = tuple()
  min_dist = N * 2
  
  # commuter_listの各要素に対して、リスト外含めて全ての要素との距離を求める
  for commuter in commuter_list:
    xh, yh = home_list[commuter]
    xw, yw = workplace_list[commuter]
    for i in range(len(home_list)):
      if i == commuter:
        continue
      xh2, yh2 = home_list[i]
      xw2, yw2 = workplace_list[i]
      dist = manhattan_distance(xh, yh, xh2, yh2) + manhattan_distance(xw, yw, xw2, yw2)
      # 家または職場同士の距離が2以下の場合は、距離を-5000する
      if manhattan_distance(xh, yh, xh2, yh2):
        dist -= 5000
      if manhattan_distance(xw, yw, xw2, yw2):
        dist -= 5000
      if dist < min_dist:
        min_dist = dist
        nearest_commuters = (commuter, i)

  return nearest_commuters

# 建設をグリッドに反映
def reflect_construction(grid: list, construction_queue: list) -> list:
  for construction in construction_queue:
    construction_type, x, y = construction
    grid[y][x] = construction_type

  return grid

# すでに敷かれた線路を避けた最短経路を求める
def get_path_bfs(x1: int, y1: int, x2: int, y2: int, grid: list) -> list:
  path = []
  next_pos_list = [[[-1, -1] for _ in range(N)] for _ in range(N)]  # 次に移動する座標
  visited = [[False] * N for _ in range(N)]  # 訪れたかどうか
  # bfsで最短経路を求める
  visited[x2][y2] = True
  queue = [(x2, y2)]
  while queue:
    x, y = queue.pop(0)
    if x == x1 and y == y1:
      break
    # 上下左右に移動
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
      next_x, next_y = x + dx, y + dy
      if grid[next_y][next_x] == [EMPTY] and not visited[next_y][next_x]:
        visited[next_y][next_x] = True
        queue.append((next_x, next_y))
        next_pos_list[next_x][next_y] = [x, y]
  # 経路を求める
  path.append((STATION, x1, y1))
  prev_x, prev_y = x1, y1
  x, y = next_pos_list[x1][y1]
  while x != x2 or y != y2:
    # 先程の移動がx軸正の方向だった場合
    if prev_x < x:
      # 次の移動がx軸正の方向の場合、縦向きの線路を敷設
      if x < next_pos_list[x][y][0]:
        path.append((RAIL_VERTICAL, x, y))
      # 次の移動がx軸負の方向の場合 (ありえないのでエラー)
      if next_pos_list[x][y][0] < x:
        raise ValueError
      # 次の移動がy軸正の方向の場合、右と上を結ぶ曲がり角を設置
      if y < next_pos_list[x][y][1]:
        path.append((RAIL_RIGHT_UP, x, y))
      # 次の移動がy軸負の方向の場合、左と上を結ぶ曲がり角を設置
      if next_pos_list[x][y][1] < y:
        path.append((RAIL_LEFT_UP, x, y))
    # 先程の移動がx軸負の方向だった場合
    if x < prev_x:
      # 次の移動がx軸負の方向の場合、縦向きの線路を敷設
      if next_pos_list[x][y][0] < x:
        path.append((RAIL_VERTICAL, x, y))
      # 次の移動がx軸正の方向の場合 (ありえないのでエラー)
      if x < next_pos_list[x][y][0]:
        raise ValueError
      # 次の移動がy軸正の方向の場合、右と下を結ぶ曲がり角を設置
      if y < next_pos_list[x][y][1]:
        path.append((RAIL_RIGHT_DOWN, x, y))
      # 次の移動がy軸負の方向の場合、左と下を結ぶ曲がり角を設置
      if next_pos_list[x][y][1] < y:
        path.append((RAIL_LEFT_DOWN, x, y))
    # 先程の移動がy軸正の方向だった場合
    if prev_y < y:
      # 次の移動がy軸正の方向の場合、横向きの線路を敷設
      if y < next_pos_list[x][y][1]:
        path.append((RAIL_HORIZONTAL, x, y))
      # 次の移動がy軸負の方向の場合 (ありえないのでエラー)
      if next_pos_list[x][y][1] < y:
        raise ValueError
      # 次の移動がx軸正の方向の場合、左と下を結ぶ曲がり角を設置
      if x < next_pos_list[x][y][0]:
        path.append((RAIL_LEFT_DOWN, x, y))
      # 次の移動がx軸負の方向の場合、左と上を結ぶ曲がり角を設置
      if next_pos_list[x][y][0] < x:
        path.append((RAIL_LEFT_UP, x, y))
    # 先程の移動がy軸負の方向だった場合
    if y < prev_y:
      # 次の移動がy軸負の方向の場合、横向きの線路を敷設
      if next_pos_list[x][y][1] < y:
        path.append((RAIL_HORIZONTAL, x, y))
      # 次の移動がy軸正の方向の場合 (ありえないのでエラー)
      if y < next_pos_list[x][y][1]:
        raise ValueError
      # 次の移動がx軸正の方向の場合、右と下を結ぶ曲がり角を設置
      if x < next_pos_list[x][y][0]:
        path.append((RAIL_RIGHT_DOWN, x, y))
      # 次の移動がx軸負の方向の場合、右と上を結ぶ曲がり角を設置
      if next_pos_list[x][y][0] < x:
        path.append((RAIL_RIGHT_UP, x, y))
    # 次の座標に移動
    prev_x, prev_y = x, y
    x, y = next_pos_list[x][y]

  # ic(x1, y1, x2, y2, path)
  return path


# 2点間の経路を求める
def get_path02(x1: int, y1: int, x2: int, y2: int, grid: list) -> list:
  # ic(x1, y1, x2, y2)
  path = []
  # 2点間のマンハッタン距離が2以下なら、空配列を返す
  if manhattan_distance(x1, y1, x2, y2) <= 2:
    return path
  # (x1, y1)が線路上なら、そこを駅にする
  if grid[y1][x1] != [EMPTY]:
    path.append((STATION, x1, y1))
    return path
  # (x1, y1)から(x2, y2)への経路を求める
  path = get_path_bfs(x1, y1, x2, y2, grid)
  
  # ic(x1, y1, x2, y2, path)
  return path

# ターン毎の建設シミュレーション
def construct(construction_queue: list, money: int, income: int, income_count: int, t: int) -> list:
  ans_list = []  # ターン毎の建設リスト
  current_income = 0  # 収入

  # ターン毎の建設シミュレーション
  for i in range(t):
    # 建設リストが空の場合
    if len(construction_queue) == 0:
      ans_list.append([DO_NOTHING])
      continue

    current_construction = construction_queue[0]
    # 資金が足りない場合
    if money < COSTS[current_construction[0]]:
      ans_list.append([DO_NOTHING])
    # 資金が足りる場合
    else:
      # ic(i, money, COSTS[current_construction[0]])
      money -= COSTS[current_construction[0]]
      ans_list.append(current_construction)
      construction_queue.pop(0)
      income_count -= 1
      # 路線が完成した場合、収入を加算
      if income_count == 0:
        current_income += income
    # 集金
    money += current_income

  return ans_list

def main():
  n, m, k, t = map(int, input().split())  # n: マスの縦と横の数(50固定), m: 住民の数, k: 最初の資金, t: ターン数(800固定)
  money = k  # 資金
  home_list = []  # 住民の家の座標
  workplace_list = []  # 住民の職場の座標
  for i in range(m):
    xh, yh, xw, yw = map(int, input().split())
    home_list.append((xh, yh))
    workplace_list.append((xw, yw))
  
  # グリッドの初期化
  grid = [[[EMPTY] for _ in range(N)] for _ in range(N)]
  # ic(grid[1][6])

  construction_queue = []  # ターン毎の建設リスト

  # 現在の資金で建てられる通勤経路を列挙
  commuter_list = get_commuter_list(money, home_list, workplace_list)

  # その中で、家同士・職場同士の距離が最も近い住民との距離が最も近い組を求める
  nearest_commuters = get_nearest_commuters(commuter_list, home_list, workplace_list)

  ic(home_list[nearest_commuters[0]], home_list[nearest_commuters[1]])
  ic(workplace_list[nearest_commuters[0]], workplace_list[nearest_commuters[1]])

  # 最初の住民の家と職場を結ぶ最短経路を求める
  construction_queue = get_path01(home_list[nearest_commuters[0]][0], home_list[nearest_commuters[0]][1], workplace_list[nearest_commuters[0]][0], workplace_list[nearest_commuters[0]][1])
  income_count = len(construction_queue)
  income = income_count - 1  # 収入は路線の長さ-1

  # 建設をグリッドに反映
  grid = reflect_construction(grid, construction_queue)

  # 次の住民の家と前の住民の家・職場をそれぞれ結ぶ最短経路を求める
  construction_queue += get_path02(home_list[nearest_commuters[1]][0], home_list[nearest_commuters[1]][1], home_list[nearest_commuters[0]][0], home_list[nearest_commuters[0]][1], grid)
  construction_queue += get_path02(workplace_list[nearest_commuters[1]][0], workplace_list[nearest_commuters[1]][1], workplace_list[nearest_commuters[0]][0], workplace_list[nearest_commuters[0]][1], grid)

  # 建設をグリッドに反映
  # grid = reflect_construction(grid, construction_queue)  # 現在は不要

  # ic(construction_queue)

  # ターン毎の建設シミュレーション
  ans_list = construct(construction_queue, money, income, income_count, t)

  # 建設リストを出力
  for construction in ans_list:
    print(*construction)


if __name__ == "__main__":
  main()