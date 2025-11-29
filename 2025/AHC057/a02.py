import os
from typing import Tuple, List
import sys

MyPC = os.path.basename(__file__) != "Main.py"
MyPC = False
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

SIZE_LIMIT = 2  # この大きさ以上の連結成分はM個までしか作らない

class UnionFind:
  # n個の頂点がすべて孤立した状態で初期化
  def __init__(self, n):
    self.parent_list = [-1] * n
    self.size_list = [1] * n

  # xが属する根付き木の根を返す
  def root(self, x):
    # xの親が-1ならxが根
    if self.parent_list[x] == -1:
      return x
    # xの親が-1でなければ、再帰的に親をたどって根を探す
    self.parent_list[x] = self.root(self.parent_list[x])  # パス圧縮
    return self.parent_list[x]
  
  # xとyが同じ根を持つかどうかを判定
  def is_same(self, x, y):
    return self.root(x) == self.root(y)
  
  # xの属する根付き木とyの属する根付き木を併合
  def unite(self, x, y):
    root_x = self.root(x)
    root_y = self.root(y)
    
    # すでに同じ根を持つ場合は何もしない
    if root_x == root_y:
      return None
    
    # 根のサイズを比較して、小さい方を大きい方に結合
    if self.size_list[root_x] < self.size_list[root_y]:
      root_x, root_y = root_y, root_x  # root_xを常に大きい方にする
    self.parent_list[root_y] = root_x  # root_yをroot_xの子にする
    self.size_list[root_x] += self.size_list[root_y]  # root_xのサイズにroot_yのサイズを加える
    self.size_list[root_y] = 0  # root_yが根ではなくなったのでサイズを0にする。この操作は必要ないが、明示的にサイズを管理するために行う
    return None

  # xの属する根付き木のサイズを返す
  def size(self, x):
    return self.size_list[self.root(x)]

# 指定した時間における、指定した点の座標を返す関数
def move_single_point(point_coords: List[List[float]], velocities: List[List[float]], uf: UnionFind, current_time: int, time: int, point_id: int, L: int) -> Tuple[float, float]:
  x, y = point_coords[point_id]
  vx, vy = velocities[uf.root(point_id)]
  current_x = x + vx * (time - current_time)
  current_x = current_x % L  # トーラス状の空間を考慮
  current_y = y + vy * (time - current_time)
  current_y = current_y % L  # トーラス状の空間を考慮
  return current_x, current_y

# 2点間の距離を返す関数
def distance_between_points(point1: Tuple[float, float], point2: Tuple[float, float], L: int) -> float:
  distance_x = abs(point1[0] - point2[0])
  distance_y = abs(point1[1] - point2[1])
  # トーラス状の空間を考慮
  distance_x = min(distance_x, L - distance_x)
  distance_y = min(distance_y, L - distance_y)
  distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
  return distance

# 指定した時間における、すべての点の座標を更新する関数
def move_all_points(point_coords: List[List[float]], velocities: List[List[float]], uf: UnionFind, current_time: int, time: int, L: int) -> None:
  N = len(point_coords)
  for i in range(N):
    x, y = point_coords[i]
    vx, vy = velocities[uf.root(i)]  # 連結成分ごとに同じ速度ベクトルを使う
    current_x = x + vx * (time - current_time)
    current_x = current_x % L  # トーラス状の空間を考慮
    current_y = y + vy * (time - current_time)
    current_y = current_y % L  # トーラス状の空間を考慮
    point_coords[i][0] = current_x
    point_coords[i][1] = current_y

# 指定した時間における、指定した点に最も近いL個の点のインデックスを返す関数
def get_nearest_points_at_time(point_coords: List[List[float]], velocities: List[List[float]], uf: UnionFind, current_time: int, time: int, point_id: int, num_points: int, L: int, K: int, M: int, large_components_count: int) -> List[int]:
  N = len(point_coords)
    # x, y = point_coords[point_id]
    # vx, vy = velocities[point_id]
  current_x, current_y = move_single_point(point_coords, velocities, uf, current_time, time, point_id, L)

  distances: List[Tuple[float, int]] = []  # (距離, インデックス)のタプルのリスト
  for i in range(N):
    if i == point_id:  # 自分自身は無視
      continue
    if uf.is_same(point_id, i):  # 同じ連結成分に属している点は無視
      continue
    if uf.size(point_id) + uf.size(i) > K:  # 結合後のサイズがKを超える場合は無視
      continue
    if uf.size(point_id) < SIZE_LIMIT and uf.size(i) < SIZE_LIMIT and uf.size(point_id) + uf.size(i) >= SIZE_LIMIT and large_components_count >= M:  # 新たにSIZE_LIMIT以上の連結成分を作れない場合は無視
      continue
    # x_i, y_i = point_coords[i]
    # vx_i, vy_i = velocities[i]
    current_x_i, current_y_i = move_single_point(point_coords, velocities, uf, current_time, time, i, L)
    distance = distance_between_points((current_x, current_y), (current_x_i, current_y_i), L)
    distances.append((distance, i))
  
  distances.sort()  # 距離でソート
  nearest_points = [distances[i][1] for i in range(min(num_points, len(distances)))]  # 最も近いnum_points個の点のインデックスを取得
  return nearest_points

# 指定した2点を結合し、そのときの距離を返す関数
def connect_points(uf: UnionFind, point_coords: List[List[float]], velocities: List[List[float]], point_id_1: int, point_id_2: int, K: int, L: int) -> float:
  if uf.size(point_id_1) + uf.size(point_id_2) > K:  # 結合後のサイズがKを超える場合は結合しない
    return None
  if uf.is_same(point_id_1, point_id_2):  # すでに同じ連結成分に属している場合は結合しない
    print("Already connected", file=sys.stderr)
    return None  # すでに同じ連結成分に属している場合は結合しない

  x1, y1 = point_coords[point_id_1]
  x2, y2 = point_coords[point_id_2]
  distance = distance_between_points((x1, y1), (x2, y2), L)
  # 速度ベクトルの更新（質量保存の法則に基づく）
  new_velocity = [(velocities[point_id_1][0] * uf.size(point_id_1) + velocities[point_id_2][0] * uf.size(point_id_2)) / (uf.size(point_id_1) + uf.size(point_id_2)),
                  (velocities[point_id_1][1] * uf.size(point_id_1) + velocities[point_id_2][1] * uf.size(point_id_2)) / (uf.size(point_id_1) + uf.size(point_id_2))]
  uf.unite(point_id_1, point_id_2)
  root = uf.root(point_id_1)
  velocities[root] = new_velocity  # 新しい根に速度ベクトルを設定
  return distance

def main():
  N, T, M, K, L = map(int, input().split())  # N: 点の数(300固定), T: 時間(1000固定), M: 目標連結成分数(10固定), K: 目標サイズ(30固定), L: 空間の一辺の長さ(10^5固定)
  uf = UnionFind(N)  # Union-Findの初期化
  point_coords: List[List[float]] = []  # 各点の座標を格納するリスト [[x1, y1], [x2, y2], ...]
  velocities: List[List[float]] = []  # 各点の速度ベクトルを格納するリスト [[vx1, vy1], [vx2, vy2], ...]

  # 入力の読み込み
  for _ in range(N):
    x, y, vx, vy = map(float, input().split())
    point_coords.append([x, y])
    velocities.append([vx, vy])

  # 3クロックごとに連結成分を増やす戦略
  current_time = 0
  large_components_count = 0  # SIZE_LIMIT以上の連結成分の数
  sum_cost = 0.0  # 総コスト
  for i in range((K-1)*M):  # 290回の繰り返し
    # 連結可能な最も距離の近い2点を探す O(N^2)の計算が必要
    min_distance = float("inf")
    point_id_1 = -1
    point_id_2 = -1
    for j in range(N):
      nearest_points = get_nearest_points_at_time(point_coords, velocities, uf, current_time, current_time, j, 1, L, K, M, large_components_count)  # 各点に対して最も近い1点を探す
      for np in nearest_points:  # 今回は1点しか入らないが、将来の拡張のためにループにしておく
        distance = distance_between_points(point_coords[j], point_coords[np], L)
        if distance < min_distance:  # 最小距離の更新
          min_distance = distance
          point_id_1 = j
          point_id_2 = np

    # 見つけた2点を結合
    if point_id_1 != -1 and point_id_2 != -1:
      # SIZE_LIMIT以上の連結成分の数を更新
      if uf.size(point_id_1) < SIZE_LIMIT and uf.size(point_id_2) < SIZE_LIMIT and uf.size(point_id_1) + uf.size(point_id_2) >= SIZE_LIMIT:
        large_components_count += 1
      elif uf.size(point_id_1) >= SIZE_LIMIT and uf.size(point_id_2) >= SIZE_LIMIT:
        large_components_count -= 1

      sum_cost += connect_points(uf, point_coords, velocities, point_id_1, point_id_2, K, L)
      print(f"{current_time} {point_id_1} {point_id_2}")  # 結合操作を出力
    else:
      print("No connectable points found", file=sys.stderr)

    # 3クロック進める
    move_all_points(point_coords, velocities, uf, current_time, current_time + 3, L)
    current_time += 3
    if current_time >= T:
      print("Reached time limit", file=sys.stderr)
      break

  # 総コストを表示（デバッグ用）
  print("Total cost:", sum_cost, file=sys.stderr)
  # 各rootの大きさを表示（デバッグ用）
  root_sizes = []
  for i in range(N):
    if uf.root(i) == i:
      root_sizes.append(uf.size(i))
  print("Final root sizes:", root_sizes, file=sys.stderr)

if __name__ == "__main__":
  main()