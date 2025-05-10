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
  n = int(input())
  a_list = list(map(int, input().split()))

  # cum_sum_list = [0]*n

  tmp_sum = sum(a_list)
  ic(tmp_sum)

  ans = 0

  for i in range(n):
    tmp_sum -= a_list[i]
    ans += a_list[i] * tmp_sum

  print(ans)


if __name__ == "__main__":
  main()