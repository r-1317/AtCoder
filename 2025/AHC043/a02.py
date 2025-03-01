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
def get_path(x1: int, y1: int, x2: int, y2: int) -> list:
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

# 現在の資金で建てられる通勤経路の中で、x座標の最大値が最小の通勤経路を求める
def get_min_x_path(money: int, home_list: list, workplace_list: list) -> list:
  min_x = N  # x座標の最大値の最小値
  min_x_path = []  # x座標の最大値の最小の通勤経路
  min_x_commuter = None  # x座標の最大値の最小の通勤経路の住民番号
  income = 0  # 路線が完成した場合の収入

  # 住民の家と職場を結ぶ最短経路を求める
  for i in range(len(home_list)):
    xh, yh = home_list[i]
    xw, yw = workplace_list[i]
    tmp_max_x = max(xh, xw)
    # 住民の家と職場を結ぶ最短経路の長さを求める
    path_dist = manhattan_distance(xh, yh, xw, yw)
    # 費用を計算
    cost = COST_STATION * 2 + COST_RAIL * path_dist
    # 費用が資金より小さい場合
    if cost <= money:
      # x座標の最大値が最小の場合
      if tmp_max_x < min_x:
        min_x = tmp_max_x
        min_x_commuter = i

  # x座標の最大値が最小の通勤経路の建設順のリストを作成
  if min_x_commuter is not None:
    xh, yh = home_list[min_x_commuter]
    xw, yw = workplace_list[min_x_commuter]
    min_x_path = get_path(xh, yh, xw, yw)
    income = manhattan_distance(xh, yh, xw, yw)

  return min_x,  min_x_path, income

# すべての通勤経路の中で、x座標の最小値が最大の通勤経路を求める
def get_max_x_path(workplace_list: list, home_list: list, min_x: int) -> list:
  max_x = -1  # x座標の最小値の最大値
  max_x_path = []  # x座標の最小値の最大の通勤経路
  max_x_commuter = None  # x座標の最小値の最大の通勤経路の住民番号

  # 住民の家と職場を結ぶ最短経路を求める
  for i in range(len(home_list)):
    xh, yh = home_list[i]
    xw, yw = workplace_list[i]
    tmp_min_x = min(xh, xw)
    # x座標の最小値が最大の場合
    if max_x < tmp_min_x:
      max_x = tmp_min_x
      max_x_commuter = i

  # x座標の最小値が最大の通勤経路の建設順のリストを作成
  if max_x_commuter is not None:
    xh, yh = home_list[max_x_commuter]
    xw, yw = workplace_list[max_x_commuter]
    max_x_path = get_path(xh, yh, xw, yw)

  return max_x, max_x_path

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
      ic(i, money, COSTS[current_construction[0]])
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
  grid = [[EMPTY] * N for _ in range(N)]

  construction_queue = []  # ターン毎の建設リスト

  # x座標の最大値が最小の通勤経路を建設リストに追加
  min_x, min_x_path, income = get_min_x_path(money, home_list, workplace_list)
  construction_queue  += min_x_path
  income_index = len(min_x_path)
  
  # x座標の最小値が最大の通勤経路を建設リストに追加
  max_x, max_x_path = get_max_x_path(workplace_list, home_list, min_x)
  construction_queue  += max_x_path

  ic(income, income_index)

  # ターン毎の建設シミュレーション
  ans_list = construct(construction_queue, money, income, income_index, t)

  # 結果の出力
  for ans in ans_list:
    print(*ans)

if __name__ == "__main__":
  main()