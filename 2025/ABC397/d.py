import os
import math
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
  n = int(input())

  for i in range(1, 10**7):
    cubed_i = i**3
    cubed_j = n + cubed_i

    float_j = int(math.pow(cubed_j, 1/3))
    # if MyPC and i == 11:
    #   ic(cubed_i, cubed_j, float_j)

    for d in range(-1, 2):
      tmp_j = int(float_j + d)
      if tmp_j**3 == cubed_j:
        print(tmp_j, i)
        sys.exit()

  print(-1)

if __name__ == "__main__":
  main()