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
  N = int(input())
  h_list = list(map(int, input().split()))

  hq = []
  heapq.heapify(hq)
  ans_list = [0]*N
  for i in range(N-2, -1, -1):
    while hq and hq[0] < h_list[i+1]:
      heapq.heappop(hq)
    heapq.heappush(hq, h_list[i+1])
    ans_list[i] = len(hq)

  print(*ans_list)

if __name__ == "__main__":
  main()