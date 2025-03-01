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

# 現在の資金で建てられる最長の通勤経路を求める
def get_longest_path(money: int, home_list: list, workplace_list: list) -> list:

  max_path_dist = 0  # 最長の通勤経路の長さ
  max_path = []  # 最長の通勤経路
  max_commuter = None  # 最長の通勤経路の住民番号

  # 住民の家と職場を結ぶ最短経路を求める
  for i in range(len(home_list)):
    xh, yh = home_list[i]
    xw, yw = workplace_list[i]
    # 住民の家と職場を結ぶ最短経路の長さを求める
    path_dist = manhattan_distance(xh, yh, xw, yw)
    # 費用を計算
    cost = COST_STATION * 2 + COST_RAIL * path_dist
    # 費用が資金より小さいく、最長の通勤経路の長さより大きい場合
    if cost <= money and max_path_dist < path_dist:
      max_path_dist = path_dist
      max_commuter = i

  # 最長の通勤経路の建設順のリストを作成
  if max_commuter is not None:
    xh, yh = home_list[max_commuter]
    xw, yw = workplace_list[max_commuter]
    max_path = get_path(xh, yh, xw, yw)

  ic(max_commuter)

  return max_path

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

  construction_list = []  # ターン毎の建設リスト

  # 現在の資金で建てられる最長の通勤経路を求める
  construction_list = get_longest_path(money, home_list, workplace_list)

  # 建設リストの残りを埋める
  construction_list += [[DO_NOTHING] for _ in range(T - len(construction_list))]

  # 建設リストを出力
  for construction in construction_list:
    print(*construction)


if __name__ == "__main__":
  main()