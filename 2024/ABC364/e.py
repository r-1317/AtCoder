import os

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def dp(a, b, dp_list):
  new_dp_list = [arr[:] for arr in dp_list]

  for i in range(10001):
    for j in range(80):
      if i + a < 10001 and dp_list[i][j] != 10**5:
        new_dp_list[i+a][j+1] = min(dp_list[i+a][j+1], dp_list[i][j]+b)

  return new_dp_list

def main():
  n, a_lim, b_lim = map(int, input().split())
  a_b_list = [list(map(int, input().split())) for _ in range(n)]

  dp_list = [[10**5]*81 for _ in range(10001)]

  for i in range(10001):
    dp_list[i][0] = 0

  for i in range(n):
    dp_list = dp(a_b_list[i][0], a_b_list[i][1], dp_list)
    # print(*dp_list[a_lim])

  ans = 0

  for j in range(1, 81):
    if dp_list[a_lim][j] <= b_lim:
      ans = j

  print(min(ans+1,n))

if __name__ == "__main__":
  main()

