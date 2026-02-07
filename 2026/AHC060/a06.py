import os
from typing import Tuple, List
import random
from typing import Optional
import time

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

start_time = time.time()

random.seed(1317)

# 定数
N = 100
K = 10
T = 10000

# 方針03用の定数
P = 0.02  # ランダムに選ぶ確率

TIME_LIMIT = 1.9  # 秒

def calc_score(outputs: List[int]) -> int:
  """出力列をシミュレーションしてスコアを返す。

  outputs:
    - v (0 <= v < N): 行動1で頂点vへ移動（木なら収穫、店なら納品）
    - -1: 行動2（現在位置の木を W -> R に変更）

  注意:
    - この関数は隣接リストを受け取らないため、辺の妥当性チェックは行わない。
    - 不正な出力列（範囲外、戻り禁止違反、赤化不可など）の場合は大きな負値を返す。
  """

  red = [False] * N  # 木の赤化状態（ショップは無視）
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

  max_score = -1
  best_outputs: List[int] = []

  while time.time() < start_time + TIME_LIMIT:
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

    score = calc_score(outputs)
    if score > max_score:
      max_score = score
      best_outputs = outputs[:]
      ic(score)
  ic(max_score)

  # 出力
  for v in best_outputs:
    print(v)


if __name__ == "__main__":
  main()