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
  N, M, S, T = map(int, input().split())
  S -= 1
  T -= 1
  adj_list = [[] for _ in range(N)]
  for _ in range(M):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    adj_list[a].append([b, 1])
  for i in range(N):
    adj_list[i].sort()
    if adj_list[i]:
      adj_list[i][0][1] = 0  # 最小のやつのコストを0にする


  # https://atcoder.jp/contests/abc362/submissions/78881091
  # たぶんAI使ってなかったと思うけれど念の為url貼っておく
  dist_list = [10**18]*N
  hq = [(0, S)]
  heapq.heapify(hq)
  while hq:
    dist, u = heapq.heappop(hq)
    if dist < dist_list[u]:
      dist_list[u] = dist
      for v, d in adj_list[u]:
        heapq.heappush(hq, (dist + d, v))

  if dist_list[T] < 10**18:
    ans = dist_list[T]
  else:
    ans = -1
  print(ans)


if __name__ == "__main__":
  main()