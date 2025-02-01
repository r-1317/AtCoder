import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  n, w = map(int, input().split())
  col_list = [[] for _ in range(w)]  # x座標ごとの、その列に存在するブロックのy座標のリスト
  block_dict = {}  # ブロックの座標をkey、そのブロックの番号をvalueとする辞書
  for i in range(n):
    x, y = map(int, input().split())
    x, y = x - 1, y - 1  # 0-indexedに変換
    col_list[x].append(y)
    block_dict[(x, y)] = i
  # すべての列について、y座標でソート
  min_len = 10**9
  for col in col_list:
    col.sort()
    min_len = min(min_len, len(col))  # 定数倍高速化の対象
  remove_list = []  # ブロックを消す時刻のリスト
  for i in range(min_len):
    max_y = -1
    for col in col_list:
      max_y = max(max_y, col[i])  # 定数倍高速化の対象
    remove_list.append(max_y)
  ic(remove_list)
  # 各ブロックの消される時刻を求める
  remove_time_list = [10**18] * n  # ブロックiが消される時刻
  for i in range(w):
    for j in range(min_len):
      coord = (i, col_list[i][j])
      block_num = block_dict[coord]
      remove_time_list[block_num] = remove_list[j]
  ic(remove_time_list)
  # クエリに答える
  q = int(input())
  for _ in range(q):
    t, a = map(int, input().split())
    t, a = t - 1, a - 1  # 0-indexedに変換
    if t < remove_time_list[a]:
      print("Yes")
    else:
      print("No")


if __name__ == "__main__":
  main()