import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  n = int(input())  # モンスターの数
  a_list = list(map(int, input().split()))  # 得られる経験値のリスト

  dp_list = [[0, 0] for _ in range(n)]  # dp[i]について、dp[i][0]偶数番目に倒した場合の最大経験値、dp[i][1]奇数番目に倒した場合の最大経験値

  dp_list[0][1] = a_list[0]  # 奇数番目に倒した場合の最大経験値

  for i in range(1, n):
    a = a_list[i]
    # 偶数にする場合
    dp_list[i][0] = max(dp_list[i-1][0], dp_list[i-1][1] + a*2)
    # 奇数にする場合
    dp_list[i][1] = max(dp_list[i-1][1], dp_list[i-1][0] + a)

  print(max(dp_list[n-1]))

if __name__ == "__main__":
  main()