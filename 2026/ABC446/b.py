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
  x_list = []
  for _ in range(N):
    _ = input()
    x_list.append(list(map(int, input().split())))

  juice_list = [True]*(M+1)

  for i in range(N):
    juice = 0
    for x in x_list[i]:
      if juice_list[x]:
        juice = x
        juice_list[x] = False
        break
    ic(juice)
    print(juice)

if __name__ == "__main__":
  main()