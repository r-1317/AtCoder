import sys

def main():

  n, y = map(int, input().split())  # n: 枚数、y: 金額
  ans = "-1 -1 -1"  # デフォルトは無かった場合

  # 検証開始
  for num_1000 in range(n+1):  # 0からnまでn+1回

    # 小計を追加
    tmp_1 = num_1000 * 1000
    sum_notes_1 = num_1000

    if (y - tmp_1) % 5000 == 0:  # 1万円か5千円で割り切れるか

      # 残り枚数の分配
      for num_5000 in range(n - sum_notes_1 +1):  # 残り枚数

        # 小計を追加
        tmp_2 = tmp_1 + num_5000*5000
        sum_notes_2 = sum_notes_1 + num_5000

        if tmp_2 + (n - sum_notes_2) * 10000 == y:  # 余った枚数がすべて1万円で正解になるか

          # 解答を更新
          ans = f"{n - sum_notes_2} {num_5000} {num_1000}"
          print(ans)
          sys.exit()

  # 解答を出力
  print(ans)

if __name__ == "__main__":
  main()