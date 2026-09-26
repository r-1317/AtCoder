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
  N = 3 * 10**5
  Q = 3 * 10**5

  print(N, Q)
  for i in range(Q):
    q = random.randint(1, 2)
    if q == 1:
      a = random.randint(1, N)
    else:
      a = chr(random.randint(97, 122))
    print(q, a)

if __name__ == "__main__":
  main()