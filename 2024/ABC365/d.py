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
  s = input()  # R: グー, P: パー, S: チョキ

  s_list = list(s)

  # じゃんけんの手 (あいこ, 勝ち)
  janken_dict = {
    "R": ("P", 2),
    "P": ("S", 0),
    "S": ("R", 1)
  }

  dp_list = [[0, 0, 0] for _ in range(n)] # グー, パー, チョキ

  # 1回目
  if s_list[0] == "R":
    dp_list[0][1] = 1
  elif s_list[0] == "P":
    dp_list[0][2] = 1
  elif s_list[0] == "S":
    dp_list[0][0] = 1

  for i in range(1, n):
    win = janken_dict[s_list[i]][0]  # str型
    lose = janken_dict[s_list[i]][1]  # int型

    dp_list[i][0] = max(dp_list[i-1][1], dp_list[i-1][2]) + (win == "R")
    dp_list[i][1] = max(dp_list[i-1][0], dp_list[i-1][2]) + (win == "P")
    dp_list[i][2] = max(dp_list[i-1][0], dp_list[i-1][1]) + (win == "S")

    dp_list[i][lose] = 0

    ic(i, dp_list[i])

  print(max(dp_list[-1]))\


if __name__ == "__main__":
  main()