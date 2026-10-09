import sys
from collections import deque


DIRS = ((-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R"))
MAX_HEIGHT = 8
MAX_MOVES = 100000


def main():
    data = sys.stdin.buffer.read().split()
    n, colors = map(int, data[:2])
    rows = data[2:2 + n]
    size = n * n
    floor = [False] * size
    towers = [[] for _ in range(size)]
    nests = [-1] * colors
    nest_color = [-1] * size

    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            v = i * n + j
            if cell == ord("#"):
                continue
            floor[v] = True
            if ord("a") <= cell <= ord("l"):
                towers[v].append(cell - ord("a"))
            elif ord("A") <= cell <= ord("L"):
                color = cell - ord("A")
                nests[color] = v
                nest_color[v] = color

    # 壁に当たるまで、各方向の合法な直線経路を先に列挙する。
    jumps = [[] for _ in range(size)]
    neighbors = [[] for _ in range(size)]
    for src in range(size):
        if not floor[src]:
            continue
        i, j = divmod(src, n)
        for di, dj, direction in DIRS:
            for length in range(1, MAX_HEIGHT + 1):
                ni, nj = i + di * length, j + dj * length
                if not (0 <= ni < n and 0 <= nj < n):
                    break
                dst = ni * n + nj
                if not floor[dst]:
                    break
                jumps[src].append((dst, direction, length))
                if length == 1:
                    neighbors[src].append(dst)

    # 各色について、床の隣接関係で測った巣までの距離を求める。
    distances = []
    toward = []
    for root in nests:
        dist = [-1] * size
        parent = [-1] * size
        dist[root] = 0
        queue = deque([root])
        while queue:
            v = queue.popleft()
            for u in neighbors[v]:
                if dist[u] != -1:
                    continue
                dist[u] = dist[v] + 1
                parent[u] = v
                queue.append(u)
        distances.append(dist)
        toward.append(parent)

    remaining = sum(map(len, towers))
    answer = []

    def move(src, dst, k, direction, length):
        nonlocal remaining
        tower = towers[src]
        moving = tower[k:]
        del tower[k:]
        towers[dst].extend(reversed(moving))
        for v in (src, dst):
            home = nest_color[v]
            if home >= 0:
                stack = towers[v]
                while stack and stack[-1] == home:
                    stack.pop()
                    remaining -= 1
        i, j = divmod(src, n)
        answer.append((i, j, k, direction, length))

    def homed_count(src, dst, k):
        """同じ距離評価の操作では、帰巣する匹数が多い方を選ぶ。"""
        source = towers[src]
        target = towers[dst]
        count = 0
        home = nest_color[src]
        if home >= 0:
            for index in range(k - 1, -1, -1):
                if source[index] != home:
                    break
                count += 1
        home = nest_color[dst]
        if home >= 0:
            index = k
            while index < len(source) and source[index] == home:
                count += 1
                index += 1
            if index == len(source):
                for color in reversed(target):
                    if color != home:
                        break
                    count += 1
        return count

    def direction_between(src, dst):
        si, sj = divmod(src, n)
        ti, tj = divmod(dst, n)
        if si == ti:
            return ("R", tj - sj) if tj > sj else ("L", sj - tj)
        return ("D", ti - si) if ti > si else ("U", si - ti)

    while remaining and len(answer) < MAX_MOVES:
        best_key = None
        best_move = None
        for src, source in enumerate(towers):
            h = len(source)
            if h == 0:
                continue
            for dst, direction, length in jumps[src]:
                capacity = MAX_HEIGHT - len(towers[dst])
                if capacity <= 0:
                    continue
                min_k = max(0, length - 1, h - capacity)
                delta = 0
                for k in range(h - 1, min_k - 1, -1):
                    color = source[k]
                    delta += distances[color][dst] - distances[color][src]
                    # 帰巣するスライムの距離は既に0なので、追加の補正は不要。
                    if best_key is not None and delta > best_key[0]:
                        continue
                    home_count = homed_count(src, dst, k)
                    key = (delta, -home_count, -(h - k))
                    if best_key is None or key < best_key:
                        best_key = key
                        best_move = (src, dst, k, direction, length)

        if best_move is not None and (best_key[0] < 0 or best_key[1] < 0):
            move(*best_move)
            continue

        # 距離が下がる合法手が無い場合は、空きのあるマスだけを使って帰巣を試みる。
        top_slimes = sorted(
            (distances[stack[-1]][v], v)
            for v, stack in enumerate(towers) if stack
        )
        progressed = False
        for _, src in top_slimes:
            color = towers[src][-1]
            # 選んだ1匹が帰巣するか、次の着地点が満杯になるまで運ぶ。
            while src != nests[color] and len(answer) < MAX_MOVES:
                dst = toward[color][src]
                if len(towers[dst]) == MAX_HEIGHT:
                    break
                direction, length = direction_between(src, dst)
                move(src, dst, len(towers[src]) - 1, direction, length)
                src = dst
                progressed = True
            if progressed:
                break
        if not progressed and best_move is not None:
            move(*best_move)

    sys.stdout.write("\n".join(f"{i} {j} {k} {d} {length}"
                               for i, j, k, d, length in answer))
    print(f"score: {len(answer)}", file=sys.stderr)


if __name__ == "__main__":
    main()
