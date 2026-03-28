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

def nothing():
  # 優先度付きキューの初期化
  hq = []
  heapq.heapify(hq)
  # 要素の追加
  heapq.heappush(hq, 3)
  heapq.heappush(hq, 1)
  heapq.heappush(hq, 2)
  # 最小値の取得
  min_val = heapq.heappop(hq)  # 1
  # 最小値の参照
  min_val = hq[0]  # 2
  # 最大値の取得（要素を負にして追加する）
  heapq.heappush(hq, -5)
  max_val = -heapq.heappop(hq)  # 5 (元に戻すために再度負にする)

def main():
  Q = int(input())

  hq = []
  heapq.heapify(hq)

  for _ in range(Q):
    query = list(map(int, input().split()))
    h = query[1]
    if query[0] == 1:
      heapq.heappush(hq, h)
    else:
      while len(hq) and hq[0] <= h:
        heapq.heappop(hq)
    print(len(hq))

if __name__ == "__main__":
  main()