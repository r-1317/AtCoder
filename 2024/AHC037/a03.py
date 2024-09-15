import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# 平面全体に等間隔で点を打つ##########################################


def main():
  n = int(input())  # 1000固定
  a_b_list = [list(map(int, input().split())) for _ in range(n)]  # 作りたい飲料の甘さと炭酸の強さのリスト
  a_b_list.insert(0, [0, 0])  # 0番目の飲料はすでに作られている
  # a_b_listの長さがn+1になるので、注意が必要
  # ic(a_b_list)

  # xy平面全体に等間隔で63*63個の点を打つ
  d = 10**9//63  # 1つの点の間隔

  default_list = [[[d*i, d*j] for i in range(63)] for j in range(63)]
  ic(default_list[0][0])

  # 等間隔の点の飲料を加える
  for i in range(len(default_list)):
    a_b_list.extend(default_list[i])
  ic(len(a_b_list))

  drink_set = set()  # すでに作られた飲料の甘さと炭酸の強さの集合
  drink_set.add(0)  # 0番目の飲料はすでに作られている
  # drink_tree = [[] for _ in range(n+1)]  # 飲料を作る順番の木  # 一旦は使わない
  parent_list = [0] * (n+1)  # 飲料iを作るために必要な飲料のリスト

  # それぞれの飲料について、最小コストで加工できる加工元の飲料を探す
  for i in range(1, n+1):
    a, b = a_b_list[i]
    min_cost = 10**18
    min_index = 0
    # 飲料iを作るために必要な親飲料を探す
    for j in range(len(a_b_list)):
      x, y = a_b_list[j]  # 飲料jの甘さと炭酸の強さ

      if i == j:  # 飲料iを作るために飲料iを使うことはできない
        continue
      if a < x or b < y:  # 甘さや炭酸が目的よりも強い飲料は使えない
        continue

      # 飲料jを使って飲料iを作るためのコストを計算
      cost = (a-x) + (b-y)
      if cost < min_cost:  # コストが最小のとき
        min_cost = cost
        min_index = j

    # drink_tree[min_index].append(i)
    parent_list[i] = min_index

  # 作れる飲料から順に飲料を作っていく
  # 計算量がO(n^2)でも間に合うので、2重ループで愚直に計算

  print(n + 63**2 - 1)  # 作る飲料の数 (4968で固定)

  # 等間隔の飲料を作る
  for i in range(len(default_list)):
    # 0番目は前の列の最初を親にする
    if i != 0:  # (0,0) の飲料はすでに作られている
      print(*default_list[i-1][0], end=" ")
      print(*default_list[i][0])
      drink_set.add(n + 1 + i*63)
    # それ以外は前の飲料を親にする
    for j in range(1, 63):
      print(*default_list[i][j-1], end=" ")
      print(*default_list[i][j])
      drink_set.add(n + 1 + i*63 + j)

  count = 0
  while count < n:
    for i in range(1, n+1):  # 0番目の飲料はすでに作られているので、1からスタート
      if i in drink_set:  # すでに作られた飲料はスキップ
        continue

      parent = parent_list[i]  # 親飲料のインデックス
      if not (parent in drink_set):  # 親飲料が作られていない場合はスキップ
        continue

      if i == 1:
        ic(parent)

      print(*a_b_list[parent], end=" ")
      print(*a_b_list[i])
      drink_set.add(i)
      count += 1

  # ic(parent_list)


if __name__ == "__main__":
  main()