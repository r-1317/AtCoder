import os
from typing import Tuple, List

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

N = 200

def main():
  _ = int(input())  # Nの読み込みだが、200で固定
  h_list = list(map(int, input().split()))  # 宝箱iの残り耐久値のリスト
  c_list = list(map(int, input().split()))  # 武器iの耐久値のリスト
  suitableness_matrix = [list(map(int, input().split())) for _ in range(N)]  # [i][j]: 武器iの宝箱jに対する攻撃力

  # 素手で全て開ける
  for i in range(N):
    for _ in range(h_list[i]):
      print(f"-1 {i}")

if __name__ == "__main__":
  main()