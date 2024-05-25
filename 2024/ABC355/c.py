from icecream import ic

# ビンゴかどうかを判定　　（廃止）
# # def jidge_bingo(card,a,n):

#   #縦
#   tmp_j = (a-1)%n
#   if all(card[i][tmp_j][1] for i in range(n)):
#     return True
  
#   #横
#   tmp_i = (a-1)//n
#   if all(card[tmp_i][j][1] for j in range(n)):
#     return True
  
#   #斜め
#   if tmp_i == tmp_j or tmp_i+tmp_j == n-1:
#     if all(card[i][i][1] for i in range(n)):
#       return True
#     elif all(card[i][n-i-1][1] for i in range(n)):
#       return True
  
#   #ビンゴでない
#   return False

def main():
  n, t = map(int, input().split())
  a_list = [0] + list(map(int, input().split()))  # 0番目は使わない

  card = [[[0,False]for _ in range(n)]for _ in range(n)]  # ビンゴカードの初期化

  for i in range(n):
    for j in range(n):
      card[i][j][0] = n*i+(j+1)

  # ic(card)

  count_i = [0]*n
  count_j = [0]*n
  count_naname = [0]*2  # 0:↘, 1:↙

  ans = -1

  for i in range(1, t+1):

    a = a_list[i]
    # ic(a)
    # ic((a-1)//n, (a-1)%n)
    card[(a-1)//n][(a-1)%n][1] = True

    count_i[(a-1)//n] += 1
    count_j[(a-1)%n] += 1
    if (a-1)//n == (a-1)%n:
      count_naname[0] += 1
    if (a-1)//n + (a-1)%n == n-1:
      count_naname[1] += 1


    if count_i[(a-1)//n] == n or count_j[(a-1)%n] == n or count_naname[0] == n or count_naname[1] == n:
      ans = i
      break

  # ic(card)

  print(ans)


if __name__ == "__main__":
  main()