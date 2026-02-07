import os
from typing import Tuple, List
import random

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

random.seed(1317)

# 定数
N = 100
K = 10
T = 10000

# 方針03用の定数
P = 0.02  # ランダムに選ぶ確率

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

  is_red = [False] * N  # 各頂点が赤くなっているかどうかのフラグ

  # 完全ランダムに移動
  outputs: List[int] = []
  current_pos = 0  # 最初は頂点0にいるものとする
  prev_pos = -1  # 直前の位置（最初は存在しないので-1）
  step_count = 0  # 移動回数カウント
  while step_count < T:
    # 次の移動先をランダムに決定
    candidates = adj_list[current_pos]  # 浅いコピー
    # 直前の位置に戻るのは避ける。常に候補が2つ以上あるので問題ないはず
    candidates = [v for v in candidates if v != prev_pos]
    next_pos = random.choice(candidates)
    outputs.append(next_pos)
    prev_pos = current_pos
    current_pos = next_pos
    step_count += 1
    # 頂点番号がK以上の場合、確率で赤くする
    if current_pos >= K and not is_red[current_pos]:
      if random.random() < P:
        is_red[current_pos] = True
        outputs.append(-1)
        step_count += 1

  # 出力
  for v in outputs:
    print(v)


if __name__ == "__main__":
  main()