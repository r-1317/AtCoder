# ahc046_random_obstacles.py
# 1.8 秒間ランダムに X 個の障害物を配置して最短経路を探索

import os
import random
import sys
import time
from collections import deque
from typing import List, Tuple

# ----------------  ハイパーパラメータ ----------------
X = 30                  # 配置するブロック数
TIME_LIMIT = 1.8        # sec  探索に使う時間
SEED = 0xC0FFEE         # 同じ入力で再現性が欲しいとき
# ----------------------------------------------------

random.seed(SEED)

# 方向ベクトル + 記号
DIRS = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]


def bfs(start: Tuple[int, int], goal: Tuple[int, int],
        grid: List[List[int]]) -> List[Tuple[str, str]] | None:
    """滑走込みの BFS。到達不能なら None を返す。"""
    if start == goal:
        return []

    q = deque([start])
    prev: dict[Tuple[int, int], Tuple[Tuple[int, int], str, str] | None] = {
        start: None}

    while q:
        i, j = q.popleft()

        # 1 マス移動
        for di, dj, dc in DIRS:
            ni, nj = i + di, j + dj
            if grid[ni][nj] == 0 and (ni, nj) not in prev:
                prev[(ni, nj)] = ((i, j), 'M', dc)
                q.append((ni, nj))

        # 滑走
        for di, dj, dc in DIRS:
            ni, nj = i, j
            while grid[ni + di][nj + dj] == 0:
                ni += di
                nj += dj
            if (ni, nj) != (i, j) and (ni, nj) not in prev:
                prev[(ni, nj)] = ((i, j), 'S', dc)
                q.append((ni, nj))

        if goal in prev:
            break

    if goal not in prev:
        return None

    # 経路を復元
    path: List[Tuple[str, str]] = []
    cur = goal
    while prev[cur] is not None:
        par, act, dc = prev[cur]          # type: ignore
        path.append((act, dc))
        cur = par
    path.reverse()
    return path


def solve_with_grid(grid: List[List[int]],
                    targets: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[str, str]]] | None:
    """固定グリッドで 40 目的地を巡る手順を返す。到達不能なら None."""
    cur = targets[0]
    actions: List[Tuple[str, str]] = []

    for nxt in targets[1:]:
        seg = bfs(cur, nxt, grid)
        if seg is None:                 # 行き止まり
            return None
        actions.extend(seg)
        cur = nxt

    return len(actions), actions


def main() -> None:
    n, m = map(int, sys.stdin.readline().split())
    raw = [tuple(map(int, sys.stdin.readline().split())) for _ in range(m)]
    targets = [(x + 1, y + 1) for x, y in raw]        # 1-based

    # 周囲に番兵 1 を置いた (n+2)×(n+2) グリッドの "空テンプレ"
    base = [[1] * (n + 2)]
    for _ in range(n):
        base.append([1] + [0] * n + [1])
    base.append([1] * (n + 2))

    # ブロック候補 (= 目的地でないマス)
    target_set = set(targets)
    candidates = [(i, j)
                  for i in range(1, n + 1)
                  for j in range(1, n + 1)
                  if (i, j) not in target_set]

    best_len = 10 ** 9
    best_act: List[Tuple[str, str]] = []

    st = time.perf_counter()
    trials = 0
    while time.perf_counter() - st < TIME_LIMIT:
        trials += 1
        # --- ランダムに X 個の壁を立てる -----------------------
        grid = [row[:] for row in base]
        for i, j in random.sample(candidates, X):
            grid[i][j] = 1
        # --------------------------------------------------------

        res = solve_with_grid(grid, targets)
        if res is None:
            continue
        steps, acts = res
        if steps < best_len:
            best_len = steps
            best_act = acts

    # -- 出力 ----------------------------------------------------
    for act, dc in best_act:
        print(act, dc, sep=' ')

    # デバッグ用 (提出時はコメントアウト可)
    # print(f'# trials={trials}  best={best_len}', file=sys.stderr)


if __name__ == '__main__':
    main()
