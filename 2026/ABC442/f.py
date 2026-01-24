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
  grid = [list(input()) for _ in range(N)]
  ic(grid)

  # 黒マスの個数
  x_cum_sum_list = [[-1]*N for _ in range(N)]  # 行列の行方向
  y_cum_sum_list = [[-1]*N for _ in range(N)]  # 行列の列方向

  for i in range(N):
    x_cum_sum_list[i][0] = (1 if grid[i][0] == "#" else 0)
    for j in range(1, N):
      x_cum_sum_list[i][j] = x_cum_sum_list[i][j-1] + (1 if grid[i][j] == "#" else 0)
  
  for i in range(N):
    y_cum_sum_list[0][i] = (1 if grid[0][i] == "#" else 0)
    for j in range(1, N):
      y_cum_sum_list[j][i] = y_cum_sum_list[j-1][i] + (1 if grid[j][i] == "#" else 0)

  ic(x_cum_sum_list)
  ic(y_cum_sum_list)

if __name__ == "__main__":
  main()