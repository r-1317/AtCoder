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

def dfs(adj_list, a_list, visited_list, u):
  for v in adj_list[u]:
    if visited_list[v]:
      continue

    a_list[v] = a_list[u] + 1
    visited_list[v] = True
    dfs(adj_list, a_list, visited_list, v)

  return None

def main():
  T = int(input())

  for _ in range(T):
    n, m = map(int, input().split())
    adj_list = [[] for _ in range(n)]
    ic(adj_list)

    for _ in range(m):
      u, v = map(int, input().split())
      u -= 1
      v -= 1
      ic(n, m, u, v)
      adj_list[u].append(v)
      adj_list[v].append(u)
    
    a_list = [0]*n
    visited_list = [False]*n

    visited_list[0] = True
    dfs(adj_list, a_list, visited_list, 0)

    ic(a_list)
    print(*a_list)

if __name__ == "__main__":
  main()