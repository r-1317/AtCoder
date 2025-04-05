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
  h, w = map(int, input().split())
  grid = [input() for _ in range(h)]
  a, b, c, d = map(int, input().split())

  dp_list = [[10**9] * w for _ in range(h)]

  dp_list[a-1][b-1] = 0

  

if __name__ == "__main__":
  main()