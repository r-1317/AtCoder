import os

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

def henkan(W, x, y):
  return x * W + y

def main():
  H, W = map(int, input().split())
  s_list = [(input()) for _ in range(H)]

  grid = [["."]*(W+2) for _ in range(H+2)]

  for i in range(H):
    for j in range(W):
      grid[i+1][j+1] = s_list[i][j]

  uf = UnionFind((H+2)*(W+2))


  # ~~下と右だけ~~ 全部
  for i in range(H+2):
    for j in range(W+2):
      if not(0 < i <= H and 0 < j <= W):# 範囲外なら左上とunite
        uf.unite(0, henkan(W, i, j))
      if grid[i][j] == "#":  # 黒なら左上とunite
        uf.unite(0, henkan(W, i, j))
        continue
      if i > H or j > W:
        continue
      if grid[i+1][j] == ".":
        uf.unite(henkan(W, i, j), henkan(W, i+1, j))
      if grid[i][j+1] == ".":
        uf.unite(henkan(W, i, j), henkan(W, i, j+1))

  count_set = set()

  for i in range(H+2):
    for j in range(W+2):
      count_set.add(uf.root(henkan(W, i, j)))

  # ic(list(count_set))

  print(len(list(count_set))-1)

if __name__ == "__main__":
  main()