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

  a_list = [list(input()) for _ in range(n)]  # グリッドの情報

  index_list = [[-1]*n for _ in range(n)]  # 各マスのインデックス

  for i in range(n):
    for j in range(n):
      pass


  for a  in a_list:
    print(*a, sep="")


if __name__ == "__main__":
  main()