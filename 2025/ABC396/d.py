import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def solve(u, w, x, n, adj_list, visited_list):
  x = x ^ w
  if u == n-1:
    return x
  
  min_ans = 10**50

  for v, w in adj_list[u]:
    if visited_list[v]:
      continue
    tmp_visited_list = visited_list[:]
    tmp_visited_list[v] = True
    ans = solve(v, w, x, n, adj_list, tmp_visited_list)
    if ans < min_ans:
      min_ans = ans

  return min_ans

def main():
  n, m = map(int, input().split())
  adj_list = [[] for _ in range(n)]

  for _ in range(m):
    u, v, w = map(int, input().split())
    u, v = u-1, v-1
    adj_list[u].append((v, w))
    adj_list[v].append((u, w))

  visited_list = [False]*n
  visited_list[0] = True

  ans = solve(0, 0, 0, n, adj_list, visited_list[:])

  print(ans)

if __name__ == "__main__":
  main()