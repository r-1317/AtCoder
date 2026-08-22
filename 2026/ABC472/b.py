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
  l_list = list(map(int, input().split()))

  cum_sum_list = [0]*(N+1)

  for i, l in enumerate(l_list):
    cum_sum_list[i+1] = cum_sum_list[i] + l

  ans = 10**9

  for i in range(1, N+1):
    left = cum_sum_list[i] - cum_sum_list[0]
    right = cum_sum_list[-1] - cum_sum_list[i]
    if abs(left - right) < ans:
      ans = abs(left - right)

  print(ans)

if __name__ == "__main__":
  main()