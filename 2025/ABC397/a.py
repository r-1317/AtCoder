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

  if 38.0 <= x:
    print(1)
  elif 37.5 <= x:
    print(2)
  else:
    print(3)

if __name__ == "__main__":
  main()