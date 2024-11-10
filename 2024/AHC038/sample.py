import random

random.seed(42)
DX = [0, 1, 0, -1]
DY = [1, 0, -1, 0]
DIR = ['R', 'D', 'L', 'U']

# 入力を読み込む
N, M, V = map(int, input().split())
s = [list(map(int, list(input()))) for _ in range(N)]
t = [list(map(int, list(input()))) for _ in range(N)]

# 木を設計する
tree = [[0, 1]]
print(len(tree) + 1)
for p, L in tree:
    print(p, L)


# 初期位置を決める
rx, ry = 0, 0
print(rx, ry)

dir1 = 0 # 辺 (0, 1) の向き
holding = False # たこ焼きを持っているかどうか

for turn in range(100):
    S = []
    # ランダムに移動する
    dir = random.randint(0, 3)
    dx, dy = DX[dir], DY[dir]
    if 0 <= rx + dx < N and 0 <= ry + dy < N:
        rx += dx
        ry += dy
        S.append(DIR[dir])
    else:
        S.append('.')
    # ランダムに回転する
    rot = random.randint(0, 2)
    if rot == 0:
        S.append('.')
    elif rot == 1:
        S.append('L')
        dir1 = (dir1 + 3) % 4
    else:
        S.append('R')
        dir1 = (dir1 + 1) % 4
    # たこ焼きを取るか置くか
    x, y = rx + DX[dir1], ry + DY[dir1]
    change = False
    if 0 <= x and x < N and 0 <= y and y < N:
        if s[x][y] == 1 and t[x][y] == 0 and not holding:
            change = True
            s[x][y] = 0
            holding = True
        elif s[x][y] == 0 and t[x][y] == 1 and holding:
            change = True
            s[x][y] = 1
            holding = False
    S.append('.') # 頂点 0 (根) は葉ではない
    if change:
        S.append('P')
    else:
        S.append('.')
    # コマンドを出力する
    print(''.join(S))
