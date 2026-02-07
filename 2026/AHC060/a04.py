import os
from typing import Tuple, List, Optional
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

def calc_score(outputs: List[int], is_red: List[bool]) -> int:
  """出力列をシミュレーションしてスコアを返す。

  outputs:
    - v (0 <= v < N): 行動1で頂点vへ移動
    - -1: 行動2（現在位置の木を W -> R に変更）

  is_red:
    初期状態で赤い木の指定。長さが N の場合は頂点ごと、長さが (N-K) の場合は木(K..N-1)のみ。
    それ以外の長さの場合は「全て白」として扱う。
  """

  # 初期の赤状態を構築（ショップは無視）
  red = [False] * N
  if len(is_red) == N:
    for i in range(K, N):
      red[i] = bool(is_red[i])
  elif len(is_red) == N - K:
    for i in range(K, N):
      red[i] = bool(is_red[i - K])

  # 各ショップの在庫集合
  inventories = [set() for _ in range(K)]

  pos = 0
  prev_move_from: Optional[int] = None  # 直前の行動1の移動元
  cone_chars: List[str] = []

  for out in outputs:
    if out == -1:
      # 行動2: 現在位置が白い木のときのみ可
      if not (K <= pos < N) or red[pos]:
        return -10**18
      red[pos] = True
      continue

    v = out
    if not (0 <= v < N):
      return -10**18
    if prev_move_from is not None and v == prev_move_from:
      return -10**18

    prev_move_from = pos
    pos = v

    if pos < K:
      inventories[pos].add("".join(cone_chars))
      cone_chars.clear()
    else:
      cone_chars.append('R' if red[pos] else 'W')

  return sum(len(inventories[i]) for i in range(K))

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

  # 完全ランダムに移動
  outputs: List[int] = []
  current_pos = 0  # 最初は頂点0にいるものとする
  prev_pos = -1  # 直前の位置（最初は存在しないので-1）
  step_count = 0  # 移動回数カウント
  for _ in range(T - (N - K)):  # 赤くするターン分を除外
    # 次の移動先をランダムに決定
    candidates = adj_list[current_pos]  # 浅いコピー
    # 直前の位置に戻るのは避ける。常に候補が2つ以上あるので問題ないはず
    candidates = [v for v in candidates if v != prev_pos]
    next_pos = random.choice(candidates)
    outputs.append(next_pos)
    prev_pos = current_pos
    current_pos = next_pos

  turn_to_red_list = [-1] * (N - K)  # outputのこのターンが終わった直後に頂点iを赤くする。つまり、実際の出力のターン数とは異なる

  # 現在のスコアを計測
  score = calc_score(outputs, turn_to_red_list)
  ic(score)

  # 赤くするターンを挟む
  # あとでやる

  # 出力
  for v in outputs:
    print(v)


if __name__ == "__main__":
  main()