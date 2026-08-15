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
  Q, V = map(int, input().split())

  hq = []
  heapq.heapify(hq)

  for _ in range(Q):
    query = list(map(int, input().split()))
    if query[0] == 1:
      t, w = query[1], query[2]
      heapq.heappush(hq, t - w)
    elif query[0] == 2:
      t = query[1]
      if hq:
        max_battery = heapq.heappop(hq)
        print(min(V, t - max_battery))
      else:
        print(-1)

if __name__ == "__main__":
  main()