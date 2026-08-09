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
  N = int(input())

  adj_list = [[] for _ in range(N)]
  # cost_list = [[] for _ in range(N)]

  for i in range(N-1):
    a, b, x = list(map(int, input().split()))
    x -= 1
    adj_list[i].append([i+1, a])
    adj_list[i].append([x, b])
    # cost_list[i].append(a)
    # cost_list[i].append(b)

  dist_list = [10**18]*N

  hq = [(0, 0)]
  heapq.heapify(hq)

  while hq:
    dist, u = heapq.heappop(hq)
    if dist < dist_list[u]:
      dist_list[u] = dist
      for v, d in adj_list[u]:
        heapq.heappush(hq, (dist + d, v))

  print(dist_list[-1])
  ic(dist_list)


if __name__ == "__main__":
  main()