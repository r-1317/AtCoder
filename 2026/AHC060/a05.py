import os
from typing import Tuple, List, Optional
import random
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

TIME_LIMIT = 1.9  # 秒

def calc_score(outputs: List[int], turn_to_red_list: List[int]) -> int:
  """出力列を簡易シミュレーションしてスコアを返す。

  注意:
  - この関数はグラフの隣接関係を受け取っていないため、辺の妥当性チェックは行わない。
  - turn_to_red_list は長さ N-K を想定し、木 t (=K..N-1) について
    「turn_to_red_list[t-K] で指定した移動ターン i の *後* (i < cur_turn) に
    初めてその木に到達した瞬間、追加の -1 行動を行って赤化する」
    という解釈でシミュレーションする（赤化はその後の収穫にのみ影響）。
  """

  # 木ごとの赤化スケジュール（無効値は -1 扱い）
  schedule = [-1] * N
  if len(turn_to_red_list) == N - K:
    for t in range(K, N):
      schedule[t] = int(turn_to_red_list[t - K])

  red = [False] * N
  inventories = [set() for _ in range(K)]

  pos = 0
  prev_move_from: Optional[int] = None  # 直前の行動1の移動元
  cone_chars: List[str] = []

  for turn, v in enumerate(outputs):
    if not (0 <= v < N):
      return -10**18
    if prev_move_from is not None and v == prev_move_from:
      return -10**18

    prev_move_from = pos
    pos = v

    if pos < K:
      inventories[pos].add("".join(cone_chars))
      cone_chars.clear()
      continue

    # 木: まず現時点の色で収穫
    cone_chars.append('R' if red[pos] else 'W')

    # スケジュールされた「指定ターンの後」に初めて到達したら赤化
    s = schedule[pos]
    if s >= 0 and (turn > s) and (not red[pos]):
      red[pos] = True

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

  turn_to_red_list = [-1] * (N - K)  # outputのこのターンが終わった後にはじめて頂点K+iを訪れた際、頂点K+iを赤くする。つまり、実際の出力のターン数とは異なる
  # 現在のスコアを計測
  score = calc_score(outputs, turn_to_red_list)
  ic(score)
  max_score = score
  max_turn_to_red_list = turn_to_red_list

  turn_to_red_list = [random.randint(0, len(outputs) - 1) for _ in range(N - K)]  # とりあえずランダムに初期化
  score = calc_score(outputs, turn_to_red_list)
  ic(score)
  max_score = max(max_score, score)
  if score == max_score:
    max_turn_to_red_list = turn_to_red_list[:]

  # 赤くするターンを挟む
  # 1箇所をランダムに移動して山登り
  while time.time() - start_time < TIME_LIMIT:
    new_turn_to_red_list = max_turn_to_red_list[:]
    idx = random.randint(0, N - K - 1)
    new_turn_to_red_list[idx] = random.randint(0, len(outputs) - 1)
    score = calc_score(outputs, new_turn_to_red_list)
    if score >= max_score:
      max_score = score
      max_turn_to_red_list = new_turn_to_red_list
      turn_to_red_list = new_turn_to_red_list

  ic(max_score)

  # 出力
  # 「指定ターン後に初めてその木を訪れたとき」にだけ -1 を挿入する
  schedule = [-1] * N
  for t in range(K, N):
    schedule[t] = int(max_turn_to_red_list[t - K])

  red = [False] * N
  pos = 0

  for turn, v in enumerate(outputs):
    print(v)
    pos = v

    if pos < K:
      continue

    s = schedule[pos]
    if s >= 0 and (turn > s) and (not red[pos]):
      print(-1)
      red[pos] = True


if __name__ == "__main__":
  main()