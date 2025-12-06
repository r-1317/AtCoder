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

sys.setrecursionlimit(3*10**5)

def dfs(adj_list, v2_list, tmp_v):
  if v2_list[tmp_v]:
    return None
  
  v2_list[tmp_v] = True

  ic(adj_list[tmp_v])

  for new_v in adj_list[tmp_v]:
    dfs(adj_list, v2_list, new_v)
  return None

def main():
  N, M = map(int, input().split())
  adj_list = [[] for _ in range(N)]  # 逆向きの辺を格納

  v2_list = [False] * N

  for i in range(M):
    x, y = map(int, input().split())
    x -= 1
    y -= 1
    adj_list[y].append(x)  # 本来とは逆向き

  Q = int(input())
  for i in range(Q):
    type, v = map(int, input().split())
    # ic(type, v)
    v -= 1

    if type == 1:
      dfs(adj_list, v2_list, v)
    
    elif type == 2:
      print("Yes" if v2_list[v] else "No")

  ic(adj_list)
  ic(v2_list)


if __name__ == "__main__":
  main()