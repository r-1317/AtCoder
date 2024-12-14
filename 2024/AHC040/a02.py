import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

# 上位3つの組み合わせを更新する
def top3(score, ans_list, best_list):
  for i in range(3):
    if score < best_list[i][0]:
      best_list.insert(i, [score, ans_list])
      best_list.pop()
      break
  return best_list

def main():
  n, t, s = map(int, input().split())  # n: 長方形の個数, : 操作回数, s: 標準偏差
  rectangle_list = [[0]*3 for _ in range(n)]  # 長方形の  [0]: 長辺, [1]: 短辺, [2]: 回転の有無
  for i in range(n):
    w, h = map(int, input().split())
    rectangle_list[i][0] = max(w, h)
    rectangle_list[i][1] = min(w, h)
    rectangle_list[i][2] = 1 if w < h else 0  # 縦のほうが長い場合は回転する

  # m = min(t, n)  # 最大操作回数と長方形の個数の小さい方
  m = min(t, 20) # 最大操作回数と理想の実行回数の小さい方

  best_list = [[10**9, []] for _ in range(3)]  # 上位3つの組み合わせを保存するリスト

  # 1列の長方形の数を変えていく
  for i in range(1, m+1):
    # ic(i)
    ans_list = []
    # 長方形を敷き詰める
    for j in range(n):
      tmp_list = [j, rectangle_list[j][2], "U", j-1]  # [0]: 長方形の番号, [1]: 回転の有無, [2]: U or L, [3]: 一つ前の長方形の番号
      if j%i == 0:  # iの倍数の場合はリセット
        tmp_list[3] = -1
      ans_list.append(tmp_list)
    # 出力
    print(n)
    for j in range(n):
      print(*ans_list[j])
    W, H = map(int, input().split())  # 結果
    best_list = top3(W+H, ans_list, best_list)

  # 余った回数は上位3つの組み合わせを出力し、上振れを狙う
  for i in range(t - m):
    print(n)
    for j in range(n):
      print(*best_list[i%3][1][j])

if __name__ == "__main__":
  main()