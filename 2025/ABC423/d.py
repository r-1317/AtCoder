import os
from collections import deque
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
  N, K = map(int, input().split())
  dq = deque()
  for _ in range(N):
    a, b, c = map(int, input().split())
    dq.append((a, b, c))

  ans_list = []
  time = 0
  capacity = K
  customer_queue = []
  heapq.heapify(customer_queue)

  while dq:
    a, b, c = dq.popleft()
    while capacity < c:
      finish_time, finish_c = heapq.heappop(customer_queue)
      time = finish_time
      capacity += finish_c
    time = max(time, a)
    heapq.heappush(customer_queue, (time+b, c))
    capacity -= c
    ans_list.append(time)

  for ans in ans_list:
    print(ans)

if __name__ == "__main__":
  main()