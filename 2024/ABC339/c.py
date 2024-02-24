def main():
  n = int(input())
  a_list = list(map(int, input().split()))
  default = 0
  tmp = 0  # 足りない乗客数

  # 足りない乗客数を求める
  for a in a_list:
    tmp += a
    default = min(tmp, default)  # defaultの-1倍だが気にしない

  ans = default*(-1)  # -1倍の修正

  # 答えを求める
  for a in a_list:
    ans += a

  print(ans)



if __name__ == "__main__":
  main()