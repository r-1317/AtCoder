# a03.py  ―  AHC046  simple solver (obstacle trick + BFS shortest path)
import os
from collections import deque
from typing import List, Tuple

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
    from icecream import ic
    ic.disable()
else:
    def ic(*args):  # type: ignore
        return None

ic.enable() if MyPC else None
# ----------------------------------------------------------------------

DIRS = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]   # (di,dj,char)


def move03(start: List[int],
           goal: List[int],
           grid: List[List[int]]) -> List[Tuple[str, str]]:
    """
    現在位置 start から goal まで、(行動, 方向) を最短手数で列挙して返す。
    行動は 'M' (1 マス移動) or 'S' (滑走)、方向は 'UDLR'。
    """
    if start == goal:         # 既に到達
        return []

    q = deque([tuple(start)])
    prev: dict[Tuple[int, int], Tuple[Tuple[int, int], str, str] | None] = {
        tuple(start): None}

    while q:
        i, j = q.popleft()

        # 1 マス移動候補
        for di, dj, dc in DIRS:
            ni, nj = i + di, j + dj
            if grid[ni][nj] == 0 and (ni, nj) not in prev:
                prev[(ni, nj)] = ((i, j), 'M', dc)
                q.append((ni, nj))

        # 滑走候補
        for di, dj, dc in DIRS:
            ni, nj = i, j
            while grid[ni + di][nj + dj] == 0:
                ni += di
                nj += dj
            if (ni, nj) != (i, j) and (ni, nj) not in prev:
                prev[(ni, nj)] = ((i, j), 'S', dc)
                q.append((ni, nj))

        if tuple(goal) in prev:        # 早期終了
            break

    if tuple(goal) not in prev:
        raise RuntimeError('goal is unreachable')

    # 経路を復元
    path: List[Tuple[str, str]] = []
    cur = tuple(goal)
    while prev[cur] is not None:
        par, act, dc = prev[cur]          # type: ignore
        path.append((act, dc))
        cur = par
    path.reverse()
    return path


# ----------------------------------------------------------------------
def main() -> None:
    n, m = map(int, input().split())
    targets = [list(map(int, input().split())) for _ in range(m)]

    # 1-based にシフトし、番兵を持つ (n+2)×(n+2) の盤面を作る
    targets = [[x + 1, y + 1] for x, y in targets]
    grid = [[1] * (n + 2)]
    for _ in range(n):
        grid.append([1] + [0] * n + [1])
    grid.append([1] * (n + 2))

    cur = targets[0][:]        # 現在位置 (= 初期位置)
    ans: List[Tuple[str, str]] = []

    # --- 障害物 2 個を置く定型プロローグ ---------------------------
    ans.extend(move03(cur, [10, 9], grid))
    cur = [10, 9]

    ans.append(('A', 'R'))      # (10,10) をトグル
    grid[10][10] = 1            # 立てる

    ans.extend(move03(cur, [10, 1], grid))
    cur = [10, 1]

    ans.append(('A', 'D'))      # (11,1) をトグル
    grid[11][1] = 1
    # -------------------------------------------------------------

    # 目的地を順に訪問
    for idx in range(1, m):
        nxt = targets[idx]
        ans.extend(move03(cur, nxt, grid))
        cur = nxt

    # 出力
    for act, dc in ans:
        print(act, dc)


# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
