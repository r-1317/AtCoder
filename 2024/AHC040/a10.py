import os
import random
import math

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

random.seed(1317)  # シードを固定

# シグモイド関数
def sigmoid(x, s):
  a = 1/(0.5*s)  # 定数。sが大きいほどsigmoid関数の傾きが緩やかになる
  ic(x, 1 / (1 + math.exp(-x*a)))
  return 1 / (1 + math.exp(-x*a))

def main():
  n, t, s = map(int, input().split())  # n: 長方形の個数, : 操作回数, s: 標準偏差
  rectangle_list = [list(map(int, input().split())) for _ in range(n)]  # 長方形の  [0]: 横幅, [1]: 縦幅  (短編・長編は不明)

  start = max(4, int(math.sqrt(n))-3)
  end = min(n//4, int(math.sqrt(n))+5)
  # m = min(t, n)  # 
  prob = 1/8  # 逆張り回転をする確率

  # x_list = [i for i in range(start, end+1)]*100  # 1列の個数を格納した、十分に長いリスト
  # ic(x_list)

  rotation_list = [0]*n  # 回転の有無を格納するリスト
  for rectangle in rectangle_list:
    if rectangle[0] < rectangle[1]:
      rotation_list[rectangle_list.index(rectangle)] = 1
  
  best_x = 0
  min_cost = 10**18

  # 最適なxを探す
  for i in range(start, end+1):
    ans_list = []
    x = i
    # 長方形を敷き詰める
    for j in range(n):
      tmp_list = [j, rotation_list[j], "U", j-1]  # [0]: 長方形の番号, [1]: 回転の有無, [2]: U or L, [3]: 一つ前の長方形の番号
      if j%x == 0:  # xの倍数の場合はリセット
        tmp_list[3] = -1
      ans_list.append(tmp_list)
    # 出力 
    print(n)
    print("#", x)  # コメントアウト
    for j in range(n):
      print(*ans_list[j])
    # コストを受け取る
    w, h = map(int, input().split())
    cost = w+h
    # 最小コストを更新
    if cost < min_cost:
      best_x = x
      min_cost = cost

  x = best_x  # xは最適な値に固定
  prev_cost = min_cost

  # 最大操作回数まで繰り返す
  for i in range(t - len(range(start, end+1))):
    # ic(i)
    next_rotation_list = rotation_list[:]
    # 確率probで逆張り回転をする
    for j in range(n):
      if random.random() < prob:
        next_rotation_list[j] = int(not rotation_list[j])
    ans_list = []
    # 長方形を敷き詰める
    for j in range(n):
      tmp_list = [j, next_rotation_list[j], "U", j-1]  # [0]: 長方形の番号, [1]: 回転の有無, [2]: U or L, [3]: 一つ前の長方形の番号
      if j%x == 0:  # xの倍数の場合はリセット
        tmp_list[3] = -1
      
      ans_list.append(tmp_list)
    # 出力
    print(n)
    print("#", x)  # コメントアウト
    for j in range(n):
      print(*ans_list[j])
    # コストを受け取る
    w, h = map(int, input().split())
    cost = w+h
    # コストが前回よりも小さければ更新
    if cost < prev_cost:
      rotation_list = next_rotation_list[:]  # 浅いコピーでも問題ないが、念のため
      prev_cost = cost

if __name__ == "__main__":
  main()