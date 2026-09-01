import os
import heapq

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  N, M = map(int, input().split())
  a_list = list(map(int, input().split()))

  adj_list = [[] for _ in range(N)]
  for j in range(M):
    u, v, b = map(int, input().split())
    u -= 1
    v -= 1
    wu = a_list[u]
    wv = a_list[v]
    adj_list[u].append((v, b + wv))
    adj_list[v].append((u, b + wu))

  dist_list = [10**18]*N
  hq = [(0, 0)]
  heapq.heapify(hq)

  while hq:
    dist, u = heapq.heappop(hq)
    if dist < dist_list[u]:
      dist_list[u] = dist
      for v, d in adj_list[u]:
        heapq.heappush(hq, (dist + d, v))

  for d in dist_list[1:]:
    print(d + a_list[0], end = " ")
  print()


if __name__ == "__main__":
  main()