import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# 幅優先探索
def bfs(n, adj_list, start, ans_list):
  queue = [start]

  while queue:
    u = queue.pop()
    ic(u)
    for v, w in adj_list[u]:
      if ans_list[v] is not None:
        continue
      ic(v, w)
      ans_list[v] = ans_list[u] + w
      queue.append(v)

  return ans_list

def main():
  n, m = map(int, input().split())  # n: 頂点数, m: 辺の数
  adj_list = [[] for _ in range(n)]  # 隣接リスト

  for _ in range(m):
    u, v, w = map(int, input().split())  # u: 始点, v: 終点, w: 重み
    adj_list[u-1].append((v-1, w))
    adj_list[v-1].append((u-1, -w))  # 逆向きの辺は重みを反転させる

  ic(adj_list)

  ans_list = [None]*n

  for i in range(n):
    if ans_list[i] is None:
      start = i
      ans_list[i] = 0
      ans_list = bfs(n, adj_list, start, ans_list)

  print(*ans_list)

  if MyPC:  # デバッグ用
    for i in range(n):
      print(ans_list[i]+200401298, end=" ")
    print()

if __name__ == "__main__":
  main()