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
  a_list = list(map(int, input().split()))

  adj_list = [[] for _ in range(N+1)]  # 逆向きのグラフ

  for i in range(N):
    a = a_list[i]
    adj_list[a].append(i+1)  # 1-indexed

  ans_list = [-1]*(N+1)

  for i in range(N, 0, -1):
    queue = adj_list[i][:]  # 嘘。実際はstack
    next_queue = []
    while queue:
      u = queue.pop()
      if ans_list[u] == -1:
        ans_list[u] = i
        for v in adj_list[u]:
          queue.append(v)
  
  print(*ans_list[1:])


if __name__ == "__main__":
  main()