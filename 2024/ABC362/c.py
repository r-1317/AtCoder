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
  l_r_list = [list(map(int, input().split())) for _ in range(n)]

  ic(l_r_list)

  ans_list = [0]*n  # ansはl以上r以下の範囲の任意の整数

  for i in range(n):
    ans_list[i] = l_r_list[i][0]

  ic(ans_list)

  sum_ans = sum(ans_list)

  ic(sum_ans)

  # sum_ansを0にするため、ansを変更する
  for i in range(n):
    if sum_ans < 0:
      tmp = ans_list[i]
      ans_list[i] = min(l_r_list[i][1], ans_list[i] + abs(sum_ans))
      sum_ans += ans_list[i] - tmp

  ic(ans_list)

  sum_ans = sum(ans_list)

  ic(sum_ans)

  if sum_ans == 0:
    print("Yes")
    print(*ans_list)
  else:
    print("No")


if __name__ == "__main__":
  main()