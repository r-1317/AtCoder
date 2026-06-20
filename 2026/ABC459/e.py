import os
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

kaijyou = [1]

for i in range(2, 10**6):
  kaijyou.append(kaijyou[-1] * i % 998244353)

def cmb(n, r):
  return kaijyou[n] - kaijyou[n - r]


def main():
  N = int(input())
  p_list = [0] + list(map(int, input().split()))
  c_list = list(map(int, input().split()))
  d_list = list(map(int, input().split()))

  # 0-indexedにする
  for i, p in enumerate(p_list):
    p_list[i] = p-1

  childs = [[] for _ in range(N)]

  for i, p in enumerate(p_list):
    if p == -1:
      continue
    childs[p].append(i)

  bfs_queue  = childs[0][:]
  queue = [0] + bfs_queue[:]
  while bfs_queue:
    new_bfs_queue = []
    for u in bfs_queue:
      new_bfs_queue.extend(childs[u])
    queue.extend(new_bfs_queue)
    bfs_queue = new_bfs_queue

  candies_counts = c_list[:]  # 浅いコピーでも良さそう?
  ans = 1
  prime = 998244353

  while queue:
    i = queue.pop()
    cand = candies_counts[i]
    d = d_list[i]
    if d > cand:
      ic(i, cand)
      print(0)
      sys.exit()
    ans *= cmb(cand, d)
    ans %= prime
    parent = p_list[i]
    if parent >= 0:
      candies_counts[parent] += cand - d

  print(ans)

if __name__ == "__main__":
  main()