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
  n, m = map(int, input().split())  # n: 休憩所の数, 距離がmの倍数の休憩所の数を求める
  a_list = list(map(int, input().split()))# a_list: 休憩所同士の距離

  dist_list = [0] * n  # 休憩所1からの距離のリスト

  dist_list[0] = a_list[0]

  for i in range(1, n):
    dist_list[i] = dist_list[i-1] + a_list[i]

  ic(dist_list)

  ans = 0

  for i in range(n):
    tmp = 0
    for j in range(n-1):
      tmp += a_list[(i+j)%n]

      if tmp % m == 0:
        ans += 1

  print(ans)

if __name__ == "__main__":
  main()