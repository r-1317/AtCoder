import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# 以前作ったやつ
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

def main():
  N, M = map(int, input().split())
  u_v_list = [list(map(int, input().split())) for _ in range(M)]

  max_cost = 0
  for i in range(1, M+1):
    max_cost += 2**i  # Pythonならではの技? C++知らんからわからんけれども

  uf = UnionFind(N+1)  # 頂点0は存在しないものとみなす

  tree_count = N  # Uni-n-Findの木の数

  sub_cost = 0  # 減らす分のコスト。多分subは英語として間違っている

  for i in range(M-1, -1, -1):  # 逆順に回す
    u, v = u_v_list[i]
    if tree_count > 2:
      if not uf.is_same(u, v):
        tree_count -= 1
      uf.unite(u, v)
      sub_cost += 2**(i+1)
    else:
      if uf.is_same(u, v):
        uf.unite(u, v)
        sub_cost += 2**(i+1)

  print((max_cost - sub_cost)%998244353)


if __name__ == "__main__":
  main()