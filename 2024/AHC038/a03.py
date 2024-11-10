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

# 現在地から最も近いたこ焼きまたは目的地の座標を返す
def find_nearest(grid_list, coord):
  x, y = coord
  nearset = [-1, -1]  # 最も近いたこ焼きまたは目的地の座標
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
def move(coord, dest_coord, s_list, t_list, takoyaki_count, holding_count, holding_list, v):
  command_list = ["."]*(v*2)  # このターンの操作
  # x軸の移動
  if coord[0] < dest_coord[0]:
    command_list[0] = "D"
  elif dest_coord[0] < coord[0]:
    command_list[0] = "U"
  # y軸の移動
  elif coord[1] < dest_coord[1]:
    command_list[0] = "R"
  elif dest_coord[1] < coord[1]:
    command_list[0] = "L"

  # 各頂点の座標を更新
  if command_list[0] == "R":
    coord[1] += 1
  elif command_list[0] == "L":
    coord[1] -= 1
  elif command_list[0] == "D":
    coord[0] += 1
  elif command_list[0] == "U":
    coord[0] -= 1

  # たこ焼きを取るか置くか
  x, y = coord
  # 空いている手があり、たこ焼きがある場合
  if is_takoyaki(len(s_list), s_list, x, y) and holding_count < v-2:
    for i in range(v-2):
      if not holding_list[i]:
        holding_list[i] = True
        s_list[x][y] = 0
        command_list[i+2+v] = "P"
        holding_count += 1
        break
  # 手持ちのたこ焼きがあり、目的地の場合
  elif is_goal(len(t_list), t_list, x, y) and holding_count:
    for i in range(v-2):
      if holding_list[i]:
        holding_list[i] = False
        t_list[x][y] = 0
        command_list[i+2+v] = "P"
        holding_count -= 1
        takoyaki_count += 1
        break

  print(*command_list, sep="")
  return takoyaki_count, holding_count


def main():
  n, m, v = map(int, input().split())  # n: グリッドの大きさ, m: たこ焼きの数, v: 頂点の数
  s_list = [list(map(int, list(input()))) for _ in range(n)]  # s: グリッド (0: たこ焼きなし, 1: たこ焼きあり)
  t_list = [list(map(int, list(input()))) for _ in range(n)]  # t: 目的地 (0: たこ焼きなし, 1: たこ焼きあり)

  # 初期位置 (頂点0の座標)
  rx = ry = n // 2  # グリッドの中心
  ic(rx, ry)

  coord = [rx, ry]  # 頂点0の座標

  print(v)  # 木の頂点数
  print("0 1")  # 頂点0から頂点1への辺
  for i in range(2, v):
    print(f"1 1")  # 頂点1から頂点iへの辺
  print(rx, ry)  # 初期位置

  # 2以上の頂点を0に重ねる
  for _ in range(2):
    command_list = ["."]*(v*2)  # このターンの操作
    command_list[2:v] = ["R"]*(v-2)  # 頂点2以上の頂点を頂点0に重ねる
    print(*command_list, sep="")

  holding_list = [False]*(v-2)  # たこ焼きを持っているかどうか
  holding_count = 0  # 持っているたこ焼きの数

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

  # たこ焼きを運搬する
  while takoyaki_count < m:
    while holding_count < v-2:  # たこ焼きを持てるだけ持つ
      takoyaki_coord = find_nearest(s_list, coord)  # 最も近いたこ焼きの座標
      if takoyaki_coord == [-1, -1]:  # たこ焼きがない場合
        break
      if takoyaki_coord == coord:  # たこ焼きが自分の座標の場合
        takoyaki_count, holding_count = move(coord, takoyaki_coord, s_list, t_list, takoyaki_count, holding_count, holding_list, v)  # 動かず、たこ焼きを持つ
      while coord != takoyaki_coord:  # たこ焼きまで移動
        takoyaki_count, holding_count = move(coord, takoyaki_coord, s_list, t_list, takoyaki_count, holding_count, holding_list, v)
  
    while holding_count:  # 手持ちのたこ焼きがなくなるまで
      goal_coord = find_nearest(t_list, coord)  # 最も近い目的地の座標
      while coord != goal_coord:
        takoyaki_count, holding_count = move(coord, goal_coord, s_list, t_list, takoyaki_count, holding_count, holding_list, v)

  ic(takoyaki_count)


if __name__ == "__main__":
  main()