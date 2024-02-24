a = int(input())  # 500円玉の枚数
b = int(input())  # 100円玉の枚数
c = int(input())  # 50円玉の枚数
x = int(input())  # 合計金額
ans = 0  # 何通りあるか

# 500円を一枚ずつ増やす
for num_500 in range(a+1):  # 0からaまでa+1回

  tmp = num_500*500  # その時点での小計

  if x < tmp:  # 金額オーバー
    break

  # 100円を一枚ずつ増やす
  for num_100 in range(b+1):  # 0からbまでb+1回

    if x < tmp + num_100*100:  # 金額オーバー
      break
    elif x <= tmp + num_100*100 + c*50:  # 選んだ500円玉と100円玉に50円玉を足してx円になるか
      ans += 1  # 1通り追加

# 回答の出力
print(ans)