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

  ans_list = [0]*3  # 1円玉、10円玉、100円玉の枚数

  for a in a_list:
    a = 10**6 - a
    a %= 1000  # 100で割ったあまりにする
    ans_list[2] += a // 100
    a %= 100
    ans_list[1] += a // 10
    a %= 10
    ans_list[0] += a

  print(*ans_list)

if __name__ == "__main__":
  main()