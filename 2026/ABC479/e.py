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

def dfs(N, adj_list, visited_list, size_list, u):
  visited_list[u] = True
  size = 1  # 自分は常に存在するので1スタート
  for v in adj_list[u]:
    if visited_list[v]:
      continue
    size += dfs(N, adj_list, visited_list, size_list, v)

  size_list[u] = size
  return size

def dfs2(adj_list, point_list, visited_list2, ans_list, point, u):
  ans_list[u] = point
  visited_list2[u] = True

  for v in adj_list[u]:
    if visited_list2[v]:
      continue
    new_point = point + point_list[v]
    dfs2(adj_list, point_list, visited_list2, ans_list, new_point, v)

def main():
  N = int(input())
  adj_list = [[] for _ in range(N)]
  edge_list = []
  for _ in range(N - 1):
    a, b = list(map(int, input().split()))
    a -= 1
    b -= 1
    adj_list[a].append(b)
    adj_list[b].append(a)
    edge_list.append((a, b))

  visited_list = [False]*N
  size_list = [-1]*N
  dfs(N, adj_list, visited_list, size_list, 0)

  ic(visited_list)
  ic(size_list)

  point_list = [0]*N
  for i in range(N - 1):
    a, b = edge_list[i]
    if size_list[a] > size_list[b]:  # 大きほうが根に近い
      upper = a
      lower = b
    else:
      upper = b
      lower = a

    if size_list[0] > size_list[lower] * 2:
      point_list[0] += i + 1
      point_list[lower] -= i + 1
    else:
      point_list[lower] += i + 1

  visited_list2 = [False]*N
  ans_list = [-1]*N
  dfs2(adj_list, point_list, visited_list2, ans_list, point_list[0], 0)

  print(*ans_list)

  # ic(point_list)

if __name__ == "__main__":
  main()