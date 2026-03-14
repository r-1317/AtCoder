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
  N, L, R = map(int, input().split())
  S = input()

  S = "@" + S  # [0]になんか入れる

  ic(S)

  cum_sum_list = [[0]*(N+1) for _ in range(27)]

  for i in range(1, N+1):
    for al in range(26):
      cum_sum_list[al][i] = cum_sum_list[al][i-1]
    cum_sum_list[ord(S[i])-97][i] += 1

  ic(cum_sum_list)

  ans = 0

  for i in range(1, N+1):
    al = ord(S[i]) - 97

    ans += cum_sum_list[al][min(i+R, N)] - cum_sum_list[al][min(i+L-1, N)]

  print(ans)

if __name__ == "__main__":
  main()