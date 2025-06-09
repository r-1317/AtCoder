import os
from typing import Tuple
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
  arr = [10**random.uniform(1.0, 4.0) for _ in range(10**7)]
  # ic(arr[:10])

  avg = sum(arr) / len(arr)
  ic(avg)

if __name__ == "__main__":
  main()