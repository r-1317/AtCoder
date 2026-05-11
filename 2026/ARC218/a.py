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
  a_list = [list(map(int, input().split())) for _ in range(N)]

  count_list = [[0]*(N*M + 1) for _ in range(N)]

  for i in range(N):
    for a in a_list[i]:
      count_list[i][a] += 1

  ans = (M**N) * M

  for i in range(N):
    for a in a_list[i]:
      for j in range(i+1, N):
        ans -= count_list[j][a]**(N - i - 1)

  print(ans % 998244353)

if __name__ == "__main__":
  main()