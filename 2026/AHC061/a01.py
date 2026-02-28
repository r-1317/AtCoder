import os
from typing import Tuple, List
from collections import deque

MyPC = os.path.basename(__file__) != "Main.py"
debug = False
if debug and MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if debug and MyPC else None

N = 10  # 盤面の1辺のマスの数
T = 100  # ターン数

# 次に選択できるマスの座標を返す関数
def get_next_positions(current_positions: List[Tuple[int, int]], owners: List[List[int]], player: int) -> List[Tuple[int, int]]:
  """ルールに基づき、player が次ターンに選択できる移動先候補を返す。

  - 到達可能領土: 現在位置から上下左右に隣接する「自分の領土」を経由して到達できるマス集合
  - 移動先: 到達可能領土に含まれる、または到達可能領土のいずれかに隣接
  - ただし移動先に他プレイヤーの駒が存在してはならない

  入力
  - current_positions: 各プレイヤーの現在位置 [(x, y), ...]
  - owners: 各マスの所有者 [[owner, ...], ...]
  - player: 移動するプレイヤーの番号

  出力
  - 移動先候補の座標 [(x, y), ...]（ソート済み）
  """

  sx, sy = current_positions[player]
  if not (0 <= sx < N and 0 <= sy < N):
    return []

  # 他プレイヤーの駒が存在するマス（移動先として禁止）
  occupied = set()
  for p, (x, y) in enumerate(current_positions):
    if p == player:
      continue
    occupied.add((x, y))

  # 自分の領土のみを通って BFS し、到達可能領土を列挙
  reachable = [[False] * N for _ in range(N)]
  q = deque()
  if owners[sx][sy] == player:
    reachable[sx][sy] = True
    q.append((sx, sy))

  dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
  while q:
    x, y = q.popleft()
    for dx, dy in dirs:
      nx, ny = x + dx, y + dy
      if not (0 <= nx < N and 0 <= ny < N):
        continue
      if reachable[nx][ny]:
        continue
      if owners[nx][ny] != player:
        continue
      reachable[nx][ny] = True
      q.append((nx, ny))

  # 到達可能領土＋その隣接マスを候補として列挙（重複排除）
  candidates = set()
  for x in range(N):
    for y in range(N):
      if not reachable[x][y]:
        continue
      candidates.add((x, y))
      for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < N and 0 <= ny < N:
          candidates.add((nx, ny))

  # 移動先に他プレイヤーの駒がいるマスは除外
  candidates.difference_update(occupied)

  return sorted(candidates)

# 各プレイヤーを next_positions[i] に移動させ、マスの所有者とレベルを更新する。
def move_player(current_positions: List[Tuple[int, int]], owners: List[List[int]], levels: List[List[int]], values: List[List[int]], U: int, next_positions: List[Tuple[int, int]]) -> None:
  """全プレイヤーを同時に移動させ、ターン終了後の盤面状態に更新する。

  ルール (task_a.md) に従い、以下を in-place で反映する。
  1) 全駒を next_positions に移動
  2) 競合解決（同一マスに複数駒）
  3) 生存駒による領土更新（占領/強化/攻撃）
  4) 回収された駒はターン開始時の位置に復帰

  注意:
  - values はスコア計算用で、この関数内では使用しない。
  - 入力として与えられる移動先が合法であることを前提とする。
  """

  m = len(current_positions)
  if m == 0:
    return
  if len(next_positions) != m:
    raise ValueError("next_positions length must match current_positions")

  start_positions = list(current_positions)

  # 競合判定: 目的地 -> そのマスへ移動したプレイヤー一覧
  dest_to_players = {}
  for p, (x, y) in enumerate(next_positions):
    dest_to_players.setdefault((x, y), []).append(p)

  recovered = [False] * m

  # 競合解決
  for (x, y), players in dest_to_players.items():
    if len(players) <= 1:
      continue

    cell_owner = owners[x][y]
    if cell_owner != -1 and cell_owner in players:
      # 所有者の駒のみ残し、他は回収
      for p in players:
        if p != cell_owner:
          recovered[p] = True
    else:
      # 所有者不在 or 所有者の駒がいない: 全回収
      for p in players:
        recovered[p] = True

  # 領土更新（回収されなかった駒のみ）
  for p, (x, y) in enumerate(next_positions):
    if recovered[p]:
      continue

    cell_owner = owners[x][y]
    if cell_owner == -1:
      # 占領
      owners[x][y] = p
      levels[x][y] = 1
      current_positions[p] = (x, y)
      continue

    if cell_owner == p:
      # 強化
      if levels[x][y] < U:
        levels[x][y] += 1
      current_positions[p] = (x, y)
      continue

    # 攻撃
    if levels[x][y] <= 0:
      # 入力矛盾に近いが、壊れないよう占領扱いに寄せる
      owners[x][y] = p
      levels[x][y] = 1
      current_positions[p] = (x, y)
      continue

    levels[x][y] -= 1
    if levels[x][y] == 0:
      owners[x][y] = p
      levels[x][y] = 1
      current_positions[p] = (x, y)
    else:
      # 攻撃失敗: 攻撃した駒は回収され、開始地点へ復帰
      recovered[p] = True

  # 回収された駒の復帰
  for p in range(m):
    if recovered[p]:
      current_positions[p] = start_positions[p]

# 各プレイヤーのスコアを計算する関数
def calc_player_scores(owners: List[List[int]], levels: List[List[int]], values: List[List[int]], M: int) -> List[int]:
  """各プレイヤーのスコア S_p を計算して返す。

  task_a.md の定義より、T ターン終了後のスコアは
  各プレイヤー p の全領土マス (i,j) についての総和
    S_p = sum(V[i][j] * L[i][j])  (O[i][j] == p)

  - owners: O[i][j] (-1: 無人, 0..M-1: 所有者)
  - levels: L[i][j]
  - values: V[i][j]
  """

  scores = [0] * M

  for i in range(N):
    for j in range(N):
      p = owners[i][j]
      if 0 <= p < M:
        scores[p] += values[i][j] * levels[i][j]

  return scores

# プレイヤー0と最大スコアのほかプレイヤーとのスコア比率を計算する関数
def calc_score_ratio(scores: List[int]) -> float:
  """プレイヤー0のスコアと、他プレイヤーのスコア比率を計算して返す。

  - scores: 各プレイヤーのスコア [S_0, S_1, ..., S_{M-1}]
  - 出力: S_0 と max(S_1, ..., S_{M-1}) の比率 (S_max / S_0)。
  """

  S_0 = scores[0]
  S_max = max(scores[1:]) if len(scores) > 1 else 0
  return S_0 / S_max if S_max > 0 else float('inf')

def main():
  _, M, _, U = map(int, input().split())  # M: プレイヤーの数, U: 各マスの最大レベル  NとTは固定
  values = [list(map(int, input().split())) for _ in range(N)]  # 各マスの価値
  positions = [list(map(int, input().split())) for _ in range(M)]  # 各プレイヤーの初期位置
  
  owners = [[-1] * N for _ in range(N)]  # 各マスの所有者 (-1: 無人)
  levels = [[0] * N for _ in range(N)]  # 各マスのレベル (無人なら0)

  for p, (x, y) in enumerate(positions):
    if 0 <= x < N and 0 <= y < N:
      owners[x][y] = p
      levels[x][y] = 1

  # 貪欲法で各ターンを進める
  for turn in range(T):
    next_positions = get_next_positions(positions, owners, 0)  # プレイヤー0(自分)の移動先候補を取得
    max_ratio = -1
    best_pos = None
    for pos in next_positions:
      prev_positions = [row[:] for row in positions]
      next_positions = prev_positions
      next_positions[0] = pos  # プレイヤー0を候補の位置に移動
      next_owners = [row[:] for row in owners]
      next_levels = [row[:] for row in levels]
      move_player(next_positions, next_owners, next_levels, values, U, next_positions)
      scores = calc_player_scores(next_owners, next_levels, values, M)
      ratio = calc_score_ratio(scores)
      if ratio > max_ratio:
        max_ratio = ratio
        best_pos = pos

    # 最良の移動先を選択
    if best_pos is None:
      raise ValueError("No valid moves available")
    # 出力
    print(*best_pos)
    # 実際のターン終了後の状態を取得
    tmp_positions = [list(map(int, input().split())) for _ in range(M)]  # 各プレイヤーが選択した位置 今回は使わない
    positions = [list(map(int, input().split())) for _ in range(M)]  # ターン終了後の各プレイヤーの位置
    owners = [list(map(int, input().split())) for _ in range(N)]  # ターン終了後の各マスの所有者
    levels = [list(map(int, input().split())) for _ in range(N)]  # ターン終了後の各マスのレベル

if __name__ == "__main__":
  main()