# 各桁の和を求める
def sum_digits(n):

  str_n = str(n)  # nの文字列
  digit_sum = 0

  for i in range(len(str_n)):  # nの桁数だけ繰り返す 

    digit_sum += int(str_n[i])  # i桁目を加える

  return digit_sum

# メイン処理
def main():
  n_max, a, b =list(map(int, input().split()))
  ans = 0  # 解答

  for n in range(1,n_max+1):  # 1以上n以下
    
    digit_sum = sum_digits(n)  # nの各桁の和

    if a <= digit_sum <= b:  # 各桁の和がa以上b以下

      ans += n  #解答にnを加える

  # 解答の出力
  print(ans)
if __name__ == "__main__":
  main()