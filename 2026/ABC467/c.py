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
  a_list = list(map(int, input().split()))
  b_list = list(map(int, input().split()))

  ans = 0

  dp_list = [[0, 0]  for _ in range(N)]

  dp_list[0][int(not(a_list[0]))] = 1

  for i in range(N - 1):
    b = b_list[i]

    dp_list[i+1] = dp_list[i][:]

    if b == 0:
      if a_list[i+1] == 0:
        dp_list[i+1][0] = dp_list[i][0]
        dp_list[i+1][1] = dp_list[i][1] + 1
      elif a_list[i+1] == 1:
        dp_list[i+1][0] = dp_list[i][0] + 1
        dp_list[i+1][1] = dp_list[i][1]
    elif b == 1:
      if a_list[i+1] == 0:
        dp_list[i+1][0] = dp_list[i][1]
        dp_list[i+1][1] = dp_list[i][0] + 1
      elif a_list[i+1] == 1:
        dp_list[i+1][0] = dp_list[i][1] + 1
        dp_list[i+1][1] = dp_list[i][0]

  print(min(dp_list[-1]))

  ic(dp_list)

if __name__ == "__main__":
  main()