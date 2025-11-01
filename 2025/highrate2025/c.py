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

  grid = [list(range(i*10000+1, i*10000+1+N)) for i in range(N)]

  ic(grid)

  for h in grid:
    print(*h)


if __name__ == "__main__":
  main()