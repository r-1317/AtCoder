import os

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
  n, l = map(int, input().split())  # n: 社員数(100固定), l: 掃除を行う週数(500000固定)
  t_list = list(map(int, input().split()))  # 社員ごとの理想の掃除回数

  # t_list[x]が多い順に社員をソート
  sorted_employees = sorted(range(n), key=lambda x: t_list[x], reverse=True)

  next_employee_list = [[0, 0] for _ in range(n)]  # 社員iが今週掃除を行った場合、次の週の掃除を行う社員のリスト。今週掃除を行った社員の掃除回数が奇数なら[0], 偶数なら[1]

  # next_employee_listの各要素に、次の社員を重複して選ぶ
  for i in range(n):
    next_employee_list[sorted_employees[i]][0] = sorted_employees[(i+1) % n]
    next_employee_list[sorted_employees[i]][1] = sorted_employees[(i+1) % n]

  max_employee = sorted_employees[0]  # 掃除回数が最も多い社員

  # x人おきに、next_employee_listの2つ目の社員をmax_employeeに変更
  # x, dxの最適な値を探す
  # x = 35  # xの初期値
  # ic(x)
  # dx = 8  # xの減少量

  min_cost = 10**9
  best_next_employee_list = [arr[:] for arr in next_employee_list]  # deepcopy
  best_x_start = 0
  best_dx = 0

  for x_start in range(20, 51):
    for dx in range(4, 17):
      # ic(x_start, dx)
      tmp_next_employee_list = [arr[:] for arr in next_employee_list]  # deepcopy
      current_index = 0
      x = x_start
      while current_index + x < n and 0 < x:
        current_index += x
        tmp_next_employee_list[sorted_employees[current_index]][1] = max_employee
        x -= dx
      cost = simulate(tmp_next_employee_list, t_list)
      # 最小コストを更新した場合、その時のnext_employee_listを保存
      if cost < min_cost:
        min_cost = cost
        best_next_employee_list = tmp_next_employee_list
        best_x_start = x_start
        best_dx = dx
        ic(x_start, dx, min_cost)

  # 先頭に戻る場所を+1して総当り
  # まずは先頭に戻る場所をすべて取得(最後尾は除く)
  x_return_list = []
  current_index = 0
  x = best_x_start
  while current_index + x < n and 0 < x:  # 先程のコードから流用
    current_index += x
    x_return_list.append(current_index)
    x -= best_dx

  # 最後尾が含まれているなら削除
  if x_return_list[-1] == n-1:
    x_return_list.pop()

  next_employee_list = [arr[:] for arr in best_next_employee_list]  # deepcopy

  # 総当り
  for i in range(2**len(x_return_list)):
    tmp_next_employee_list = [arr[:] for arr in next_employee_list]  # deepcopy
    for j in range(len(x_return_list)):
      if i >> j & 1:  # 1が立っている場合
        next_employee_list[x_return_list[j]][1] = next_employee_list[x_return_list[j]][0]
        next_employee_list[x_return_list[j]+1][1] = max_employee

    # x = best_x_start
    # for j in range(len(x_return_list)):
    #   if i >> j & 1:
    #     x -= best_dx

    cost = simulate(next_employee_list, t_list)
    if cost < min_cost:
      min_cost = cost
      best_next_employee_list = tmp_next_employee_list
      ic(x, min_cost)


  for arr in best_next_employee_list:
    print(*arr)

  ic(x)
  ic(simulate(best_next_employee_list, t_list))  # 確認用であり、消してもよい

if __name__ == "__main__":
  main()