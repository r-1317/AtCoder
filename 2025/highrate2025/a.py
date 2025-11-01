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
  N, M = map(int, input().split())
  s_e_list = [list(map(int, input().split())) for _ in range(N)] # S: 問題を解く時間, E: 歩く時間

  # S*M+E
  # i/(N*10)を全てに足そう

  time_list = [[0.0, i] for i in range(1, N+1)]

  for i in range(N):
    s, e = s_e_list[i]
    time = s*M + e + (i/(N*10))
    time_list[i][0] = time

  ic(time_list)

  time_list.sort()

  for ans in time_list:
    print(ans[1], end = " ")
  print()


if __name__ == "__main__":
  main()