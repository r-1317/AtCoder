import os
import bisect

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  N, K = map(int, input().split())
  adj_set_list = [set() for _ in range(N)]
  for _ in range(N-1):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    adj_set_list[a].add(b)
    adj_set_list[b].add(a)

  v_list = list(map(int, input().split()))
  for i in range(K):
    v_list[i] -= 1
  v_set = set(v_list)

  leaf_list = []
  for u in range(N):
    if len(adj_set_list[u]) == 1 and (u not in v_set):
      leaf_list.append(u)

  exits_list = [True]*N
  queue = leaf_list
  while queue:
    new_queue = []
    for a in queue:
      if not exits_list[a]:
        continue
      exits_list[a] = False
      b = list(adj_set_list[a])[0]  # ここの計算量が不安
      adj_set_list[b].remove(a)
      if len(adj_set_list[b]) == 1 and (b not in v_set):
        new_queue.append(b)
    queue = new_queue

  print(sum(exits_list))

if __name__ == "__main__":
  main()