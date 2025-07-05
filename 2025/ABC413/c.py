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
  q = int(input())

  dq = deque()  # 双方向キューを使用

  for _ in range(q):
    query = list(map(int, input().split()))
    if query[0] == 1:
      c = query[1]  # 追加する個数
      x = query[2]  # 追加する値
      dq.append([x, c])  # (値, 個数)
    elif query[0] == 2:
      k = query[1]
      total = 0
      while k:
        d = min(k, dq[0][1])
        total += d * dq[0][0]
        dq[0][1] -= d
        k -= d
        if dq[0][1] == 0:
          dq.popleft()
      ic(total)
      print(total)

if __name__ == "__main__":
  main()