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
  n, m = map(int, input().split())
  c_list = list(map(int, input().split()))

  animals_list = [[] for _ in range(n)]

  for i in range(m):
    zoo_list = list(map(int, input().split()))
    zoo_list.pop(0)
    for zoo in zoo_list:
      animals_list[zoo - 1].append(i)

  ic(animals_list)

  # bit全探索もどき
  ans = 10**18

  for i in range(3**n):
    cost = 0
    visited_list = [0] * m
    for j in range(n):
      visit_count = (i // (3**j)) % 3
      if visit_count == 0:
        continue
      cost += c_list[j]*visit_count
      for k in animals_list[j]:
        visited_list[k] += visit_count
      flag = True
      for k in range(m):
        if visited_list[k] < 2:
          flag = False
          break
      if flag:
        ans = min(ans, cost)

  print(ans)

if __name__ == "__main__":
  main()