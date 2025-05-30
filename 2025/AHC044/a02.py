import os
from typing import Tuple

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  n, l = map(int, input().split())  # n: 社員数, l: 掃除を行う週数
  t_list = list(map(int, input().split()))  # 社員ごとの理想の掃除回数

  ic(t_list)

  cleaning_count_list = [0] * n  # 社員iの掃除回数
  next_employee_list = [[0, 0] for _ in range(n)]  # 社員iが今週掃除を行った場合、次の週の掃除を行う社員のリスト。今週掃除を行った社員の掃除回数が奇数なら[0], 偶数なら[1]

  # next_employee_listの各要素に、次の社員を重複して選ぶ
  for i in range(n):
    next_employee_list[i][0] = next_employee_list[i][1] = i+1

  next_employee_list[-1][0] = next_employee_list[-1][1] = 0

  # ic(next_employee_list)

  for arr in next_employee_list:
    print(*arr)

if __name__ == "__main__":
  main()