import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  N, M, L, S, T = map(int, input().split())

  adj_list = [[] for _ in range(N)]  # Tupleを要素に持つ
  for _ in range(M):
    u, v, c = map(int, input().split())
    u -= 1
    v -= 1
    adj_list[u].append((v, c))

  ans_set = set()

  queue = [(0, 0)]  # (idx, cost)

  for _ in range(L):
    next_queue = []
    for node, cost in queue:
      for next_node, d_cost in adj_list[node]:
        ic(next_node, d_cost)
        next_queue.append((next_node, cost + d_cost))
    ic(next_queue)
    queue = next_queue

  # costの判定
  for node, cost in queue:
    if S <= cost <= T:
      ans_set.add(node + 1)  # 1_indexedに変換
      ic(node)

  ans_list = list(ans_set)
  ans_list.sort()

  print(*ans_list)

if __name__ == "__main__":
  main()