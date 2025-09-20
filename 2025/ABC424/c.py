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
  N = int(input())

  adj_list = [[] for _ in range(N)]
  queue = []
  visited_list = [False] * (N)

  for i in range(N):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    if a == b == -1:
      queue.append(i)
    else:
      adj_list[a].append(i)
      adj_list[b].append(i)

  while queue:
    v = queue.pop()
    visited_list[v] = True
    for nv in adj_list[v]:
      if not visited_list[nv]:
        queue.append(nv)

  print(sum(visited_list))

if __name__ == "__main__":
  main()