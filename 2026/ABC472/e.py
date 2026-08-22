import os
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

sys.setrecursionlimit(10**6)

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

def dfs(adj_list, visited_list, u, i):
  if visited_list[u] > -1:
    if visited_list % 2 != i % 2:  # 奇数の場合
      return [u]
    else:
      return None
  visited_list[u] = i
  for v in adj_list[u]:
    arr = dfs(adj_list, visited_list, v, i+1)
    if arr is not None:
      arr.append(u)
      return arr
  visited_list[u] = -1
  return None

def main():
  T = int(input())

  for _ in range(T):
    N, M = map(int, input().split())
    adj_list = [[] for _ in range(N)]
    uf = UnionFind(N)
    for _ in range(M):
      a, b = map(int, input().split())
      a -= 1
      b -= 1
      adj_list[a].append(b)
      adj_list[b].append(a)
      uf.unite(a, b)

    visited_root = [False]*N
    visited_list = [-1]*N

    flag = False
    for u in range(N):
      root = uf.root(u)
      if not visited_list[root]:
        ans_list = dfs(adj_list, visited_list, root, 0)
        if ans_list is not None:
          print(len(ans_list))
          print(*ans_list)
          flag = True
        visited_root[root] = True
        if flag:
          break
      if flag:
        break
    if not flag:
      print(-1)


if __name__ == "__main__":
  main()