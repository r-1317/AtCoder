import os
from typing import Tuple

N = 100
L = 500000

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def simulate(next_employee_list: list[list[int]], t_list: list[int]) -> int:
  cleaning_count_list = [0] * N  # 社員iの掃除回数
  current_employee = 0  # 今週掃除を行う社員

  # 本来はL週分のシミュレーションを行うが、ここではsim週分のシミュレーションを行う
  sim = 500000
  for i in range(sim):
    cleaning_count_list[current_employee] += 1
    if cleaning_count_list[current_employee] % 2 == 1:  # 掃除回数が奇数の場合
      current_employee = next_employee_list[current_employee][0]
    else:  # 掃除回数が偶数の場合
      current_employee = next_employee_list[current_employee][1]

  cost = 0

  for i in range(N):
    cost += abs(cleaning_count_list[i]*(L//sim) - t_list[i])

  return cost

def main():
  n, l = map(int, input().split())  # n: 社員数, l: 掃除を行う週数
  t_list = list(map(int, input().split()))  # 社員ごとの理想の掃除回数

  # t_list[x]が多い順に社員をソート
  sorted_employees = sorted(range(n), key=lambda x: t_list[x], reverse=True)

  next_employee_list = [[0, 0] for _ in range(n)]  # 社員iが今週掃除を行った場合、次の週の掃除を行う社員のリスト。今週掃除を行った社員の掃除回数が奇数なら[0], 偶数なら[1]

  # next_employee_listの各要素に、次の社員を重複して選ぶ
  for i in range(n):
    next_employee_list[sorted_employees[i]][0] = sorted_employees[(i+1) % n]
    next_employee_list[sorted_employees[i]][1] = sorted_employees[(i+1) % n]

  max_employee = sorted_employees[0]  # 掃除回数が最も多い社員

  # d人おきに、next_employee_listの2つ目の社員をmax_employeeに変更
  d = 35

  for i in range(0, n, d):
    next_employee_list[sorted_employees[i]][1] = max_employee

  for arr in next_employee_list:
    print(*arr)

  ic(d)
  ic(simulate(next_employee_list, t_list))

if __name__ == "__main__":
  main()