import os
import random

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  h = 1000
  w = 1000
  # s_list = ["#", "."]

  print(h, w)

  for i in range(h):
    for j in range(w):
      if i == 0 and j == 0:
        print("E", end="")
      else:
        print(".", end="")
    print()



if __name__ == "__main__":
  main()