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
  s_list = [input() for _ in range(n)]

  m = max([len(s) for s in s_list])

  ic(m)

  ans_list = [[""]*n for _ in range(m)]

  for i in range(n):
    for j in range(len(s_list[i])):
      ans_list[j][-(i+1)] = s_list[i][j]

  ic(ans_list)

  for i in range(m):
    for j in range(n-1, 0, -1):
      if ans_list[i][j] and not ans_list[i][j-1]:
        ans_list[i][j-1] = "*"

  for i in range(m):
    print(*ans_list[i], sep="")

if __name__ == "__main__":
  main()