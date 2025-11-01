import os
import sys

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
  mikan = N

  # # 2以下なら即勝利  # 不要
  # if N < 3:
  #   print("First")
  #   print(N)
  #   input()
  #   sys.exit()

  # すでに3の倍数なら後攻、そうでないなら先攻
  if mikan % 3 == 0:
    print("Second")
  else:
    print("First")
    x = mikan%3
    print(x)
    mikan -= x

  while True:
    a = int(input())  # 相手の手
    if a == 0:
      break
    mikan -= a
    # 自分の手番
    x = mikan%3
    print(x)
    mikan -= x


if __name__ == "__main__":
  main()