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
  n = int(input())
  a_list = list(map(int, input().split()))
  w_list = list(map(int, input().split()))

  x_list = [[0]for _ in range(n+1)]

  for i in range(n):
    x_list[a_list[i]].append(w_list[i])

  ic(x_list)

  for i in range(n+1):
    x_list[i].sort(reverse=True)

  ic(x_list)

  for i in range(n+1):
    x_list[i][0] = 0

  ic(x_list)

  ans = 0

  for i in range(n+1):
    ans += sum(x_list[i])

  print(ans)


if __name__ == "__main__":
  main()