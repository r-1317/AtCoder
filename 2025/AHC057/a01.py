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
def move_single_point(point_coords: List[List[float]], velocities: List[List[float]], current_time: int, time: int, point_id: int, L: int) -> Tuple[float, float]:
  x, y = point_coords[point_id]
  vx, vy = velocities[point_id]
  current_x = x + vx * (time - current_time)
  current_x = current_x % L  # トーラス状の空間を考慮
  current_y = y + vy * (time - current_time)
  current_y = current_y % L  # トーラス状の空間を考慮
  return current_x, current_y

# 指定した時間における、2点間の距離を返す関数
def distance_between_points(point1: Tuple[float, float], point2: Tuple[float, float], L: int) -> float:
  distance_x = abs(point1[0] - point2[0])
  distance_y = abs(point1[1] - point2[1])
  # トーラス状の空間を考慮
  distance_x = min(distance_x, L - distance_x)
  distance_y = min(distance_y, L - distance_y)
  distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
  return distance

# 指定した時間における、指定した点に最も近いL個の点のインデックスを返す関数
def get_nearest_points_at_time(point_coords: List[List[float]], velocities: List[List[float]], uf: UnionFind, current_time: int, time: int, point_id: int, num_points: int, L: int) -> List[int]:
  N = len(point_coords)
  x, y = point_coords[point_id]
  vx, vy = velocities[point_id]
  current_x, current_y = move_single_point(point_coords, velocities, current_time, time, point_id, L)

  distances: List[Tuple[float, int]] = []  # (距離, インデックス)のタプルのリスト
  for i in range(N):
    if i == point_id:  # 自分自身は無視
      continue
    if uf.is_same(point_id, i):  # 同じ連結成分に属している点は無視
      continue
    x_i, y_i = point_coords[i]
    vx_i, vy_i = velocities[i]
    current_x_i, current_y_i = move_single_point(point_coords, velocities, current_time, time, i, L)
    distance = distance_between_points((current_x, current_y), (current_x_i, current_y_i), L)
    distances.append((distance, i))
  
  distances.sort()  # 距離でソート
  nearest_points = [distances[i][1] for i in range(min(num_points, len(distances)))]  # 最も近いnum_points個の点のインデックスを取得
  return nearest_points

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

  # 時刻0ですべての結合を行う
  for i in range(M):
    # まず、どの点とも結合されていない点を見つける
    base_point = -1
    for j in range(N):
      if uf.size(j) == 1:
        base_point = j
        break
    if base_point == -1:
      ValueError("結合されていない点が見つかりません。")
    # まだ結合していない点のうち、base_pointに最も近いK-1個の点を見つけて結合する
    nearest_points = get_nearest_points_at_time(point_coords, velocities, uf, 0, 0, base_point, N-1, L)
    for np in nearest_points:
      if uf.size(base_point) >= K:  # すでにK個結合している場合は終了
        break
      if uf.size(np) != 1:  # 相手がすでに結合している場合はスキップ
        continue
      uf.unite(base_point, np)
      print(f"0 {base_point} {np}")  # 結合操作を出力

if __name__ == "__main__":
  main()