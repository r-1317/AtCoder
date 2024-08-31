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
  a, b = map(int, input().split())
  if a == b:
    print(1)
  elif (a - b) % 2 == 0:
    print(3)
  else:
    print(2)

if __name__ == "__main__":
  main()