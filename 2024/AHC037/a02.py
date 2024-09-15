import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# x,y軸上に等間隔で点を打つ##########################################


def main():
  n = int(input())  # 1000固定
  a_b_list = [list(map(int, input().split())) for _ in range(n)]  # 作りたい飲料の甘さと炭酸の強さのリスト
  a_b_list.insert(0, [0, 0])  # 0番目の飲料はすでに作られている
  # a_b_listの長さがn+1になるので、注意が必要
  # ic(a_b_list)

  # x軸上とy軸上に等間隔で点を打つ
  x_axis_list = [[i*5*10**5, 0] for i in range(1, 2001)]
  y_axis_list = [[0, i*5*10**5] for i in range(1, 2001)]

  # 座標の最大値を10**9未満にする
  x_axis_list[-1][0] -= 1
  y_axis_list[-1][1] -= 1
  ic(x_axis_list[-1], y_axis_list[-1])

  a_b_list += x_axis_list + y_axis_list

  ic(len(a_b_list))

  drink_set = set()  # すでに作られた飲料の甘さと炭酸の強さのセット
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

  print(5000)  # 作る飲料の数 (5000で固定)

  # x軸上の飲料を作る
  print(*a_b_list[0], end=" ")
  print(*x_axis_list[0])
  drink_set.add(n+1)
  for i in range(2, 2001):
    print(*a_b_list[n+i-1], end=" ")
    print(*a_b_list[n+i])
    drink_set.add(n+i)
  # y軸上の飲料を作る
  print(*a_b_list[0], end=" ")
  print(*y_axis_list[0])
  drink_set.add(n+2001)
  for i in range(2002, 4001):
    print(*a_b_list[n+i-1], end=" ")
    print(*a_b_list[n+i])
    drink_set.add(n+i)

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