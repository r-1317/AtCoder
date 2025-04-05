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
  a = int(input())

  b = 400 // a

  print(b if a*b == 400 else -1)

if __name__ == "__main__":
  main()