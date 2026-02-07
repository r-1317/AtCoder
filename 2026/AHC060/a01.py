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

# 定数
N = 100
K = 10
T = 10000

def main():
  _, M, _, _ = map(int, input().split())  # N: 頂点の数, M: 辺の数, K: アイス屋の数, T: ターン数  M以外は定数なので無視
  adj_list: List[List[int]] = [[] for _ in range(N + 1)]  # 隣接リストの初期化
  for _ in range(M):
    a, b = map(int, input().split())
    adj_list[a].append(b)
    adj_list[b].append(a)
  
  # ~~この後に座標が入力されるが、使用しないので無視~~
  # やっぱりアイス屋の位置は必要なのでK(=10)行だけ読み込む
  ice_shops: List[Tuple[int, int]] = []
  for _ in range(K):
    x, y = map(int, input().split())
    ice_shops.append((x, y))

  

if __name__ == "__main__":
  main()