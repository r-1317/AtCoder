import os
from typing import Tuple
import random as r
import time

N = 100
L = 500000
EMPLOYEES = tuple(range(N))

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

r.seed(1317)

def simulate(next_employee_list: list[list[int]], t_list: list[int]) -> int:
  cleaning_count_list = [0] * N  # 社員iの掃除回数
  current_employee = 0  # 今週掃除を行う社員

  # 本来はL週分のシミュレーションを行うが、ここではsim週分のシミュレーションを行う
  sim = 10000
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
  start_time = time.time()  # 開始時刻

  n, l = map(int, input().split())  # n: 社員数(100固定), l: 掃除を行う週数(500000固定)
  t_list = list(map(int, input().split()))  # 社員ごとの理想の掃除回数。長さn

  # ic(t_list)

  next_employee_list = [[0, 0] for _ in range(n)]  # 社員iが今週掃除を行った場合、次の週の掃除を行う社員のリスト。今週掃除を行った社員の掃除回数が奇数なら[0], 偶数なら[1]

  # next_employee_listの各要素をランダムに選ぶ。重複しても良い。
  for i in range(n):
    next_employee_list[i][0] = r.randrange(n)
    next_employee_list[i][1] = r.randrange(n)

  # ic(next_employee_list)

  min_cost = simulate(next_employee_list, t_list)
  # ic(min_cost)

  count = 0  # デバッグ用の試行回数カウンタ

  m = 200  # 1回の試行で変更する社員の数

  # next_employee_listの各要素をm個ずつ変更して、山登り法で最適解を探す。これを1.9秒間繰り返す
  while time.time() - start_time < 1.9:
    new_next_employee_list = [arr[:] for arr in next_employee_list]  # deep copy

    random_index_list = r.sample(range(200), m)  # ランダムにm個のインデックスを選ぶ。2で割った値が社員番号、2で割った余りが0なら[0], 1なら[1]　ここは重複なし

    # next_employee_listの各要素をm個ずつ変更する
    for index in random_index_list:
      employee = index // 2
      new_next_employee_list[employee][index % 2] = r.randrange(n)

    cost = simulate(new_next_employee_list, t_list)
    if MyPC and count%100 == 0 and False:
      ic(count, cost)

    if cost < min_cost:
      min_cost = cost
      next_employee_list = new_next_employee_list

    count += 1

  for arr in next_employee_list:
    print(*arr)

  ic(m)
  ic(count)
  ic(min_cost)
  ic(time.time() - start_time)

if __name__ == "__main__":
  main()