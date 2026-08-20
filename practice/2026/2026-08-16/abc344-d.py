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
  T = input()
  N = int(input())
  s_list = [list(input().split())[1:] for _ in range(N)]

  dp_list =[[10**9]*(len(T)+1) for _ in range(N+1)]
  dp_list[0][0] = 0

  for i in range(1, N+1):
    for j in range(len(T)+1):
      dp_list[i][j] = dp_list[i-1][j]
    row = s_list[i-1]
    for s in row:
      for k in range(len(T) - len(s), -1, -1):
        if T[k: k + len(s)] == s:
          dp_list[i][k + len(s)] = min(dp_list[i][k + len(s)], dp_list[i-1][k] + 1)

  print(dp_list[-1][-1] if dp_list[-1][-1] != 10**9 else -1)


if __name__ == "__main__":
  main()