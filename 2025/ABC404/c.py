import os
from collections import defaultdict

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None



def main():
  n, m = map(int, input().split())
  adj_list = [[] for _ in range(n)]
  count_list = [0] * n
  for i in range(m):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    adj_list[a].append(b)
    adj_list[b].append(a)
    count_list[a] += 1
    count_list[b] += 1

  flag = True
  for i in range(n):
    if count_list[i] != 2:
      flag = False
      break

  if not flag:
    print("No")
    exit()

  visited_list = [False] * n
  visited_count = 0
  prev_node = 0
  next_node = adj_list[0][0]
  visited_list[0] = True
  adj_list[next_node].remove(prev_node)
  prev_node = next_node
  visited_count += 1
  visited_list[next_node] = True

  while visited_count < n:
    if len(adj_list[next_node]) == 0:
      print("No")
      ic(adj_list)
      exit()
    next_node = adj_list[next_node][0]
    visited_list[next_node] = True
    visited_count += 1
    if prev_node in adj_list[next_node]:
      adj_list[next_node].remove(prev_node)
    else:
      print("No")
      ic(adj_list)
      exit()
    prev_node = next_node

  ic(prev_node)
  
  if prev_node != 0:
    ic(adj_list)
    print("No")
    exit()
  print("Yes")



if __name__ == "__main__":
  main()