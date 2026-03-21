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
  X = input()
  Y = input()
  Q = int(input())

  for _ in range(Q):
    l, r, c = map(int, input().split())

if __name__ == "__main__":
  main()