import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# https://github.com/r-1317/AtCoder/blob/main/library.py
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

def bfs(grid, H, W, x, y):
  ans = 1
  visited_set = set()
  visited_set.add((x, y))
  queue = [(x, y)]
  while queue:
    new_queue = []
    for x, y in queue:
      for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if not(0 <= nx < H and 0 <= ny < W) or grid[nx][ny] == "#" or (nx, ny) in visited_set:
          continue
        ans += 1
        visited_set.add((nx, ny))
        if grid[nx][ny] == ".":
          new_queue.append((nx, ny))
    queue = new_queue

  return ans



def main():
  H, W = map(int, input().split())
  grid = [list(input()) for _ in range(H)]

  for x in range(H):
    for y in range(W):
      c = grid[x][y]
      if c == "#":
        for dx, dy in DIRS:
          nx, ny = x + dx, y + dy
          if 0 <= nx < H and 0 <= ny < W and grid[nx][ny] == ".":
            grid[nx][ny] = "x"

  uf = UnionFind(H*W)

  for x in range(H):
    for y in range(W):
      c = grid[x][y]
      if c == ".":
        for dx, dy in DIRS:
          nx, ny = x + dx, y + dy
          if 0 <= nx < H and 0 <= ny < W and grid[nx][ny] == ".":
            uf.unite(x*W + y, nx*W + ny)

  ans = 1
  for x in range(H):
    for y in range(W):
      idx = x * W + y
      if uf.root(idx) == idx and grid[x][y] == ".":
        ans = max(ans, bfs(grid, H, W, x, y))

  print(ans)

if __name__ == "__main__":
  main()