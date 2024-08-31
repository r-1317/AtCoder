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
  diff_list = [0] * (n-1)  # a_list[i] - a_list[i-1]のリスト

  for i in range(1, n):
    diff_list[i-1] = a_list[i] - a_list[i-1]

  ic(diff_list)

  ans = n  # 長さ1の数列は常に等差数列
  count = 0
  tmp = -1

  for d in diff_list:
    if d == tmp:
      count += 1
    else:
      count = 1
      tmp = d

    ans += count

  print(ans)


if __name__ == "__main__":
  main()