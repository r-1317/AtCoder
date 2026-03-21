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
  fee_list = [list(map(int, input().split())) for _ in range(N-1)]

  flag = False

  for a in range(N):
    for b in range(a+1, N):
      for c in range(b+1, N):
        through = fee_list[a][c-a-1]
        breath = fee_list[a][b-a-1] + fee_list[b][c-b-1]

        if breath < through:
          flag = True
          ic(a,b,c)

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()