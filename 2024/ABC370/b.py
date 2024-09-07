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
  a_list = [list(map(int, input().split())) for _ in range(n)]

  tmp = 1

  for i in range(1, n+1):
    x = max(tmp, i)
    y = min(tmp, i)

    tmp = a_list[x-1][y-1]

  print(tmp)

if __name__ == "__main__":
  main()