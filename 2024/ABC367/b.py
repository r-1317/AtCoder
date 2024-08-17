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
  x = float(input())

  ic(x)

  if x == int(x):
    print(int(x))
  else:
    print(x)

if __name__ == "__main__":
  main()