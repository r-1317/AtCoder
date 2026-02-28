import os
from collections import deque

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  T = int(input())
  for _ in range(T):
    N, D = map(int, input().split())
    a_list = list(map(int, input().split()))
    b_list = list(map(int, input().split()))
    egg_count = 0
    egg_queue = deque()
    for i in range(N):
      a = a_list[i]
      b = b_list[i]
      egg_count += a
      egg_queue.append([i, a])
      egg_count -= b
      e = b
      while e:
        de = min(egg_queue[0][1], e)
        e -= de
        egg_queue[0][1] -= de
        if egg_queue[0][1] <= 0:
          egg_queue.popleft()
      while egg_queue and egg_queue[0][0] <= i - D:
        egg_count -= egg_queue[0][1]
        egg_queue.popleft()
    print(egg_count)
    ic(egg_count)

if __name__ == "__main__":
  main()