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
  N, M, K = map(int,input().split())
  a_b_list = [list(map(int, input().split())) for _ in range(N)]

  dp_list = [[0]*(M+1) for _ in range(N+1)]
  last_town_list = [[-1]*(M+1) for _ in range(N+1)]

  for i in range(1, N+1):
    for j in range(M+1):
      dp_list[i][j] = dp_list[i-1][j]
      last_town_list[i][j] = last_town_list[i-1][j]

      if j > 0:
        # dp_list[i][j] = max(dp_list[i][j], dp_list[i][j-1])
        if dp_list[i][j] < dp_list[i][j-1]:
          dp_list[i][j] = dp_list[i][j-1]
          last_town_list[i][j] = last_town_list[i][j-1]

      a, b = a_b_list[i-1]
      if b <= j and i - last_town_list[i-1][j-b] <= K:
        dp_list[i][j] = max(dp_list[i][j], dp_list[i-1][j-b] + a)
        last_town_list[i][j] = i-1

  ic(dp_list)
  ic(last_town_list)

  print(dp_list[-1][-1])


if __name__ == "__main__":
  main()