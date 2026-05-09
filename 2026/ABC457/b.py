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
  l_list = [list(map(int, input().split())) for _ in range(N)]
  X, Y = map(int, input().split())

  print(l_list[X-1][Y])

if __name__ == "__main__":
  main()