import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# 辺の追加
def query1(graphs_list, u, v):
  while u != graphs_list[u][0]:
    u = graphs_list[u][0]
  while v != graphs_list[v][0]:
    v = graphs_list[v][0]

  if u == v:
    return
  
  # グラフの連結
  for i in range(10):
    graphs_list[u][1][i] = graphs_list[v][1][i+10]
  graphs_list[u][1].sort()

  for i in range(10):
    graphs_list[u][1][i] = -1

  graphs_list[v][0] = u

  # ic(v, graphs_list[u][1])


# 頂点uと連結な中からk番目に大きい頂点を出力
def query2(graphs_list, v, k):
  while v != graphs_list[v][0]:
    v = graphs_list[v][0]
  ic(v)
  ic(graphs_list[v][1])
  print(graphs_list[v][1][-k])

def main():
  n, q = map(int, input().split())
  
  graphs_list = [[i, [-1]*19 + [i]] for i in range(n+1)]

  ic()

  for _ in range(q):
    query = list(map(int, input().split()))

    if query[0] == 1:  # 辺の追加
      u, v = query[1], query[2]
      query1(graphs_list, u, v)

    else:  # 頂点uと連結な中からk番目に小さい頂点を出力
      v, k = query[1], query[2]
      query2(graphs_list, v, k)

if __name__ == "__main__":
  main()