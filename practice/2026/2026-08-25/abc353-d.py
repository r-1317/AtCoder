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
  N = int(input())
  a_list = list(map(int, input().split()))

  cum_sum_list = [0]*(N+1)  # 逆からの累積和

  for i in range(N-1, -1, -1):
    cum_sum_list[i] = cum_sum_list[i + 1] + 10**len(str(a_list[i]))
  ic(cum_sum_list)

  ans = 0

  for i, a in enumerate(a_list):
    ans += a * (cum_sum_list[i+1] + i)

  print(ans % 998244353)

if __name__ == "__main__":
  main()