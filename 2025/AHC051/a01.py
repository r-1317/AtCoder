import os
from typing import Tuple

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  N, M, K = map(int, input().split())
  processor_coord_list = [tuple(map(int, input().split())) for _ in range(N)]  # 処理装置予定地の座標
  sorter_coord_list = [tuple(map(int, input().split())) for _ in range(M)]  # 分別器の予定地の座標
  prob_list = [list(map(float, input().split())) for _ in range(K)]  # 各分別器のゴミiの転送確率

  # 出力
  print(*range(N))
  print(0)
  for _ in range(M):
    print(-1)

if __name__ == "__main__":
  main()