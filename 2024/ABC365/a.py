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
  y = int(input())

  if y % 400 == 0:
    print("366")
  elif y % 100 == 0:
    print("365")
  elif y % 4 == 0:
    print("366")
  else:
    print("365")

if __name__ == "__main__":
  main()