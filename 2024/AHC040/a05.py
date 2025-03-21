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

# シグモイド関数 (現在は不要)
def sigmoid(x, s):
  a = 1/(4*s)  # 定数。sが大きいほどsigmoid関数の傾きが緩やかになる
  ic(x, 1 / (1 + math.exp(-x*a)))
  return 1 / (1 + math.exp(-x*a))

def main():
  n, t, s = map(int, input().split())  # n: 長方形の個数, : 操作回数, s: 標準偏差
  rectangle_list = [list(map(int, input().split())) for _ in range(n)]  # 長方形の  [0]: 横幅, [1]: 縦幅  (短編・長編は不明)

  start = max(4, int(math.sqrt(n))-5)
  end = min(n//4, int(math.sqrt(n))+3)
  # m = min(t, n)  # 
  prob = 1/4  # 通常の回転をする確率

  x_list = [i for i in range(start, end+1)]*100  # 1列の個数を格納した、十分に長いリスト
  # ic(x_list)

  # 最大操作回数まで繰り返す
  for i in range(t):
    # ic(i)
    x = x_list[i]
    ans_list = []
    # 長方形を敷き詰める
    for j in range(n):
      tmp_list = [j, 0, "U", j-1]  # [0]: 長方形の番号, [1]: 回転の有無(仮に無とおく), [2]: U or L, [3]: 一つ前の長方形の番号
      if j%x == 0:  # xの倍数の場合はリセット
        tmp_list[3] = -1
      d = rectangle_list[j][1] - rectangle_list[j][0]  # 縦横の差(縦が長い場合は正)
      # まず、通常通りの回転をする
      tmp_list[1] = 1 if 0 < d else 0
      # 確率probで通常通り回転する
      tmp_list[1] = tmp_list[1] if random.random() < prob else int(not tmp_list[1])
      ans_list.append(tmp_list)
    # 出力
    print(n)
    for j in range(n):
      print(*ans_list[j])

if __name__ == "__main__":
  main()