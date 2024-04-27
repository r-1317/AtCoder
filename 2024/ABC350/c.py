from icecream import ic

def main():
  n = int(input())
  a_list = [0] + list(map(int, input().split()))  # 初期状態のリスト ([0]は無視)
  
  k = 0  # 操作回数
  q_list = [""]*n  # 操作のリスト
  pos_list = [0]*(n+1)  # 位置のリスト ([0]は無視)

  # ic(a_list)

  for i in range(1, n+1):
    # ic(i)
    pos_list[a_list[i]] = i

  # ic(pos_list)  # デバッグ

  # ソート開始
  for i in range(1, n+1):  # iがindex番号かつそこの数字

    # ic(a_list)
    # ic(q_list)

    if a_list[i] != (i):

      a_list[pos_list[i]] = a_list[i]
      a_list[i] = i

      q = f"{i} {pos_list[i]}"
      q_list[k] = q
      k += 1

  print(k)
  if k != 1:
    print(*q_list[:k], sep='\n')
  else:
    print(q_list[0])


if __name__ == "__main__":
  main()