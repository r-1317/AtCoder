from icecream import ic

def main():
  n, m, k = map(int, input().split())  # n: 鍵の数, m: テストの回数, k: 必要な鍵の数
  c_a_r_list = [list(input().split()) for _ in range(m)]# c: テストiに用いた鍵の数, a: テストiに用いた鍵の番号, r: テストiの結果

  c_list = [0]*m
  a_list = [[0]*15 for _ in range(m)]
  r_list = [0]*m

  # リストの中身を整形
  for i in range(m):
    c_list[i] = int(c_a_r_list[i][0])

    for j in range(c_list[i]):
      a_list[i][j] = int(c_a_r_list[i][1+j])

    r_list[i] = c_a_r_list[i][-1]

  # rをbool型に変換
  for i in range(len(r_list)):
    if r_list[i] == "o":
      r_list[i] = True
    else:
      r_list[i] = False

  # ic(c_list)
  # ic(a_list)
  # ic(r_list)

  ans = 0

  # 鍵の組み合わせを全探索
  for i in range(2**n):
    # 鍵の組み合わせを2進数で表現
    key_str = format(i, '016b')

    # ic(i)
    # ic(key_str)
    # ic(key_str[15:15-n:-1])

    # 鍵の組み合わせをリストに変換
    key_list = [False]*n
    l = 0

    for j in range(15, 15-n, -1):
      if key_str[j] == "1":
        key_list[l] = True
      l += 1

    # ic(key_list)

    # 正しい鍵がk個以上の場合のみ処理を行う  # 誤り。すべてのテストの結果がFalse場合もある。
    # if key_list.count(True) < k:
    #   continue

    flag = True

    # すべてのテストに対して処理を行う
    for j in range(m):
      tmp_list = [False]*n

      for l in range(c_list[j]):
        tmp_list[l] = key_list[a_list[j][l]-1]

      # ic(tmp_list)

      if (k <= tmp_list.count(True)) != r_list[j]:
        flag = False
        break

    if flag:
      ans += 1

  print(ans)


if __name__ == "__main__":
  main()