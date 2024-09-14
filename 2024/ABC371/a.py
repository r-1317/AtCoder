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
  ab, ac, bc = input().split()
  A = B = C = 0
  if ab == ">":
    A += 1
  else:
    B += 1

  if ac == ">":
    A += 1
  else:
    C += 1

  if bc == ">":
    B += 1
  else:
    C += 1

  if A == 1:
    print("A")
  elif B == 1:
    print("B")
  else:
    print("C")

if __name__ == "__main__":
  main()