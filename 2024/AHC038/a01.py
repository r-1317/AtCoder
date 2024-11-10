import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def is_takoyaki(n, s_list, x, y):
  if 0 <= x < n and 0 <= y < n:  # グリッドの範囲内かどうか
    return bool(s_list[x][y])
  return False

def is_goal(n, t_list, x, y):
  if 0 <= x < n and 0 <= y < n:  # グリッドの範囲内かどうか
    return bool(t_list[x][y])
  return False

# 部分木を回転させる
def transform(tree_list,coord_list, v, s):
  # vの親を軸にs方向に回転
  parent = tree_list[v].index(min(tree_list[v]))  # 親
  parent_coord = coord_list[parent]  # 親の座標

  # vとその子孫をすべてリストアップ
  v_list = [v]
  queue = [v]
  while queue:
    v = queue.pop(0)
    for i in range(len(tree_list[v])):
      if 0 < tree_list[v][i]:
        v_list.append(i)
        queue.append(i)

  # 回転
  for v in v_list:
    x, y = coord_list[v]
    x -= parent_coord[0]
    y -= parent_coord[1]
    # ic(v, x, y)

    # 右回転の場合
    if s == "R":
      coord_list[v][0] = parent_coord[1] + y  # x'
      coord_list[v][1] = parent_coord[0] - x  # y'
    # 左回転の場合
    elif s == "L":
      coord_list[v][0] = parent_coord[1] - y  # x'
      coord_list[v][1] = parent_coord[0] + x  # y'

# 現在地から最も近いたこ焼きまたは目的地の座標を返す
def find_nearest(grid_list, coord):
  x, y = coord
  nearset = [0, 0]  # 最も近いたこ焼きまたは目的地の座標
  dist = 10**9  # 最も近いたこ焼きまたは目的地までのマンハッタン距離

  for i in range(len(grid_list)):
    for j in range(len(grid_list[i])):
      if grid_list[i][j]:
        d = abs(x - i) + abs(y - j)
        if d < dist:
          nearset = [i, j]
          dist = d

  return nearset

# たこ焼きまたは目的地まで移動する
def move(coord_list, dest_coord, s_list, t_list, leaf_list, holding_list, turn_count, takoyaki_count):
  command_list = ["."]*(2*len(coord_list))  # このターンの操作
  # x軸の移動
  if coord_list[0][0] < dest_coord[0]:
    command_list[0] = "D"
  elif dest_coord[0] < coord_list[0][0]:
    command_list[0] = "U"
  # y軸の移動
  elif coord_list[0][1] < dest_coord[1]:
    command_list[0] = "R"
  elif dest_coord[1] < coord_list[0][1]:
    command_list[0] = "L"

  # 各頂点の座標を更新
  for i in range(len(coord_list)):
    if command_list[0] == "R":
      coord_list[i][1] += 1
    elif command_list[0] == "L":
      coord_list[i][1] -= 1
    elif command_list[0] == "D":
      coord_list[i][0] += 1
    elif command_list[0] == "U":
      coord_list[i][0] -= 1

  # ic(coord_list)

  # たこ焼きを取るか置くか
  for leaf in leaf_list:
    x, y = coord_list[leaf]
    if is_takoyaki(len(s_list), s_list, x, y) and not holding_list[leaf]:
      # ic(leaf, x, y)
      # ic(is_takoyaki(len(s_list), s_list, x, y))  
      holding_list[leaf] = True
      s_list[x][y] = 0
      command_list[leaf+len(coord_list)] = "P"
    elif is_goal(len(t_list), t_list, x, y) and holding_list[leaf]:
      holding_list[leaf] = False
      t_list[x][y] = 0
      takoyaki_count += 1
      command_list[leaf+len(coord_list)] = "P"

  print(*command_list, sep="")
  turn_count += 1
  # ic(coord_list[0], dest_coord, takoyaki_count)
  return turn_count, takoyaki_count


def main():
  n, m, v = map(int, input().split())  # n: グリッドの大きさ, m: たこ焼きの数, v: 頂点の数
  s_list = [list(map(int, list(input()))) for _ in range(n)]  # s: グリッド (0: たこ焼きなし, 1: たこ焼きあり)
  t_list = [list(map(int, list(input()))) for _ in range(n)]  # t: 目的地 (0: たこ焼きなし, 1: たこ焼きあり)

  v = 5  # 一時的に5に固定

  turn_count = 0  # 操作回数

  # 初期位置 (頂点0の座標)
  rx = ry = n // 2  # グリッドの中心
  ic(rx, ry)

  # 木を設計する
  tree_list = [[0]*v for _ in range(v)]  # 木の隣接行列
  
  for i in range(1, v):
    tree_list[0][i] = 1
    tree_list[i][0] = -1  # 親であることを示す

  coord_list = [[rx, ry], [rx,ry+1], [rx,ry+1], [rx,ry+1], [rx,ry+1]]  # 各頂点の座標 (x, y)
  leaf_list = [1, 2, 3, 4]  # 葉のリスト

  print(len(tree_list))  # 頂点の数
  for i in range(1, len(tree_list)):
    parent = tree_list[i].index(min(tree_list[i]))  # 負の値があれば親
    print(parent, abs(tree_list[i][parent]))
  print(rx, ry)  # 初期位置

  # 十字に変形する
  #   4
  #   |
  # 3-0-1
  #   |
  #   2
  command_list = ["."]*(2*v)  # このターンの操作
  transform(tree_list, coord_list, 2, "R")
  command_list[2] = "R"
  transform(tree_list, coord_list, 3, "R")
  command_list[3] = "R"
  transform(tree_list, coord_list, 4, "L")
  command_list[4] = "L"
  print(*command_list, sep="")
  turn_count += 1

  # 3は2回の回転が必要
  command_list = ["."]*(2*v)
  transform(tree_list, coord_list, 3, "R")
  command_list[3] = "R"
  print(*command_list, sep="")
  turn_count += 1

  ic(coord_list)

  # すでに目的地にあるたこ焼きを数える
  takoyaki_count = 0
  for x in range(n):
    for y in range(n):
      if is_takoyaki(n, s_list, x, y) and is_goal(n, t_list, x, y):
        takoyaki_count += 1
        # たこ焼きと目的地を消す
        s_list[x][y] = 0
        t_list[x][y] = 0

  ic(takoyaki_count)

  # ic(is_takoyaki(n, s_list, 10, 10))

  holding_list = [False]*v  # たこ焼きを持っているかどうか
  # たこ焼きを運搬する
  while turn_count < (10**5-100) and takoyaki_count + sum(holding_list) < m:  # 操作回数が10^5未満かつたこ焼きがすべて運ばれるまで (-100は余裕を持たせるため)
    takoyaki_coord = find_nearest(s_list, coord_list[0])  # 最も近いたこ焼きの座標
    takoyaki_coord[0] += 1  # 頂点4がたこ焼きを取るようにする
    if takoyaki_coord[0] == n:  # ずらした先がグリッド外の場合
      takoyaki_coord[0] -= 2  # 逆方向にずらす
    # ic(coord_list[0], takoyaki_coord)
    while coord_list[0] != takoyaki_coord:
      turn_count, takoyaki_count = move(coord_list, takoyaki_coord, s_list, t_list, leaf_list, holding_list, turn_count, takoyaki_count)
  
    goal_coord = find_nearest(t_list, coord_list[0])  # 最も近い目的地の座標
    goal_coord[0] += 1  # 頂点4が目的地にたこ焼きを置くようにする
    if goal_coord[0] == n:  # ずらした先がグリッド外の場合
      goal_coord[0] -= 2  # 逆方向にずらす
    while coord_list[0] != goal_coord:
      turn_count, takoyaki_count = move(coord_list, goal_coord, s_list, t_list, leaf_list, holding_list, turn_count, takoyaki_count)

  ic(sum(holding_list))

  # まだたこ焼きが残っている場合
  if any(holding_list):
    # すべての葉を上に移動
    command_list = ["."]*(2*v)
    transform(tree_list, coord_list, 1, "L")
    command_list[1] = "L"
    transform(tree_list, coord_list, 2, "R")
    command_list[2] = "R"
    transform(tree_list, coord_list, 3, "R")
    command_list[3] = "R"
    print(*command_list, sep="")
    turn_count += 1

    # ic(coord_list)

    # 2は2回の回転が必要
    command_list = ["."]*(2*v)
    transform(tree_list, coord_list, 2, "R")
    command_list[2] = "R"
    # destination = [coord_list[0][0]-1, coord_list[0][1]]
    # turn_count, takoyaki_count = move(coord_list, destination, s_list, t_list, leaf_list, holding_list, turn_count, takoyaki_count)
    print(*command_list, sep="")
    turn_count += 1

    x, y = coord_list[0]
    for i in range(1,v):
      coord_list[i][0] = x-1
      coord_list[i][1] = y

    ic(coord_list)

  while any(holding_list) and turn_count < (10**5-100):  # 操作回数が10^5未満かつたこ焼きがすべて運ばれるまで (-100は余裕を持たせるため)
    goal_coord = find_nearest(t_list, coord_list[0])  # 最も近い目的地の座標
    goal_coord[0] += 1  # 頂点4が目的地にたこ焼きを置くようにする
    if goal_coord[0] == n:  # ずらした先がグリッド外の場合
      goal_coord[0] -= 2  # 逆方向にずらす
      # すべての葉を下に移動
      for i in range(2):
        command_list = ["."]*(2*v)
        transform(tree_list, coord_list, 1, "R")
        command_list[1] = "R"
        transform(tree_list, coord_list, 2, "R")
        command_list[2] = "R"
        transform(tree_list, coord_list, 3, "R")
        command_list[3] = "R"
        transform(tree_list, coord_list, 4, "R")
        command_list[4] = "R"
        print(*command_list, sep="")
    while coord_list[0] != goal_coord:
      turn_count, takoyaki_count = move(coord_list, goal_coord, s_list, t_list, leaf_list, holding_list, turn_count, takoyaki_count)
    # 下に移動した葉を元に戻す
    if coord_list[0][0] < coord_list[1][0]:
      for i in range(2):
        command_list = ["."]*(2*v)
        transform(tree_list, coord_list, 1, "L")
        command_list[1] = "L"
        transform(tree_list, coord_list, 2, "L")
        command_list[2] = "L"
        transform(tree_list, coord_list, 3, "L")
        command_list[3] = "L"
        transform(tree_list, coord_list, 4, "L")
        command_list[4] = "L"
        print(*command_list, sep="")
        turn_count += 1

  ic(turn_count)



if __name__ == "__main__":
  main()