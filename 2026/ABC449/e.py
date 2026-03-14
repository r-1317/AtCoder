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
  N, M = map(int, input().split())
  a_list = list(map(int, input().split()))
  Q = int(input())

  freq_list = [0]*M

  for a in a_list:
    freq_list[a-1] += 1

  max_freq = max(freq_list)
  houwa_count = 0
  for f in freq_list:
    houwa_count += max_freq - f

  hq = [-1]*M

  for i in range(M):
    hq[i] = [freq_list[i], i+1]

  heapq.heapify(hq)

  ans_list = a_list[:]

  for _ in range(houwa_count):
    f_count, v = heapq.heappop(hq)
    ans_list.append(v)
    heapq.heappush(hq, [f_count+1, v])

  for _ in range(Q):
    x = int(input())
    x -= 1

    if x < len(ans_list):
      ic(ans_list[x])
      print(ans_list[x])
    else:
      x -= len(ans_list)

      x %= M
      x += 1
      ic(x)
      print(x)

if __name__ == "__main__":
  main()