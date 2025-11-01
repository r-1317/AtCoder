import os
import random

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

random.seed(1317)

def r(N):
  return random.randint(0, N-1)

def check(grid, N):
  sum_list = [0]*(N)

  for x in range(N):
    sum_list[x] = sum(grid[x])

  for y in range(N):
    s = 0
    for x in range(N):
      s += grid[x][y]
    sum_list.append(s)
  
  # ic(sum_list)

  ans = True
  invalid_row_idx = []
  invalid_column_idx = []

  for i in range(N):
    if sum_list.count(sum_list[i]) != 1:
      ans = False
      invalid_row_idx.append(i)

  for i in range(N):
    if sum_list.count(sum_list[N+i]) != 1:
      ans = False
      invalid_column_idx.append(i)

  if ans:
    ic(sum_list)
  
  return ans, invalid_row_idx, invalid_column_idx


def main():
  N = int(input())

  grid = [[0]*N for _ in range(N)]

  init_list = list(range(1, N**2 + 1))
  random.shuffle(init_list)

  ic(len(init_list))

  for i in range(N):
    for j in range(N):
      grid[i][j] = init_list.pop()

  ic(grid)

  is_vaild, invalid_row_idx, invalid_column_idx = check(grid, N)
  ic(is_vaild)
  ic(invalid_row_idx)
  ic(invalid_column_idx)

  # 正解するまでランダムに変更を加える
  while not(is_vaild):
    for row in invalid_row_idx:
      x1 = row
      y1 = r(N)
      x2 = r(N)
      y2 = r(N)

      a1 = grid[x1][y1]
      a2 = grid[x2][y2]

      grid[x1][y1] = a2
      grid[x2][y2] = a1

    for col in invalid_column_idx:
      x1 = r(N)
      y1 = col
      x2 = r(N)
      y2 = r(N)

      a1 = grid[x1][y1]
      a2 = grid[x2][y2]

      grid[x1][y1] = a2
      grid[x2][y2] = a1

    is_vaild, invalid_row_idx, invalid_column_idx = check(grid, N)

  for h in grid:
    print(*h)
    pass
  ic("done")
  ic(is_vaild)


if __name__ == "__main__":
  main()