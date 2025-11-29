import os
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  X, Y, Z = map(int, input().split())

  for i in range(10**6):
    if X == Y * Z:
      print("Yes")
      sys.exit()
    elif X < Y * Z:
      print("No")
      sys.exit()
    X += 1
    Y += 1

if __name__ == "__main__":
  main()