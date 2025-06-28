import os
import itertools

MyPC = os.path.basename(__file__) != "Main.py"
# MyPC = False
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def diff(n, adj_list, tmp_adj_list):
  ans = 0
  # and_list -> tmp_adj_list
  for u in range(n):
    for v in adj_list[u]:
      if v not in tmp_adj_list[u]:
        ans += 1
  
  # tmp_adj_list -> and_list
  for u in range(n):
    for v in tmp_adj_list[u]:
      if v not in adj_list[u]:
        ans += 1
  return ans

def find(adj_list, n, x, tmp_adj_list):
  if x == n:  # すべての辺を選んだ場合
    # flag = True
    # for u in range(n):
    #   for v in tmp_adj_list[u]:
    #     if u not in tmp_adj_list[v]:
    #       flag = False
    #       break
    #     tmp_adj_list[v].remove(u)  # uからvへの辺を削除
    # if not flag:  # 辺の選び方が不正な場合
    #   return 10**9
    return diff(n, adj_list, tmp_adj_list)

  min_ans = 10**9

  for i in range(n):
    if x in tmp_adj_list[i]:  # xからiへの辺がすでにある場合はスキップ
      continue
    a = min(x, i)
    b = max(x, i)
    next_tmp_adj_list = [a[:] for a in tmp_adj_list]
    next_tmp_adj_list[a].append(b)  # xからiへの辺を追加

    tmp_ans = find(adj_list, n, x + 1, next_tmp_adj_list)
    if tmp_ans < min_ans:
      min_ans = tmp_ans
  return min_ans


def main():
  n, m = map(int, input().split())
  adj_list = [[] for _ in range(n)]
  edge_set = set()
  for _ in range(m):
    a, b = map(int, input().split())
    if a > b:  # 常に a < b になるようにする
      a, b = b, a
    edge_set.add((a, b))

  edge_list = list(edge_set)
  ic(edge_set)

  all_edges = [(i, j) for i in range(n) for j in range(i + 1, n)]

  ans = 10**9

  for e in itertools.combinations(all_edges, n):
    deg_list = [0] * n
    for a, b in e:
      # if a > b:  # 常に a < b になるようにする
      #   a, b = b, a
      deg_list[a] += 1
      deg_list[b] += 1

    if any(deg != 2 for deg in deg_list):
      continue

    tmp_ans = n + m  # すべての辺を消してからn本の辺を追加する場合
    for a, b in e:
      if (a, b) in edge_set or (b, a) in edge_set:
        tmp_ans -= 2  # 消す分とつける分

    if tmp_ans < ans:
      ans = tmp_ans

  print(ans)



if __name__ == "__main__":
  main()