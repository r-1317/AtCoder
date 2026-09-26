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
  C = input()

  if C == "B":
    print("Y")
  elif C == "Y":
    print("R")
  else:
    print("B")

if __name__ == "__main__":
  main()