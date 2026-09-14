import os
import sys

# MyPC = os.path.basename(__file__) != "Main.py"
# if MyPC:
#   from icecream import ic
#   ic.disable()
# else:
#   def ic(*args):
#     return None

# ic.enable() if MyPC else None

def main():
  N, M = map(int, input().split())

  adj_list = [[] for _ in range(N)]

  for _ in range(M):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    adj_list[a].append(b)

  visited_list = [False]*N
  queue = [0]
  i = 1
  while queue:
    new_queue = []
    for u in queue:
      for v in adj_list[u]:
        if v == 0:
          ans = i
          print(ans)
          sys.exit()
        if visited_list[v]:
          continue
        new_queue.append(v)
        visited_list[v] = True
    queue = new_queue
    i += 1

  print(-1)


if __name__ == "__main__":
  main()