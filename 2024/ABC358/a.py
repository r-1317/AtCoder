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
  s = input()

  print("Yes" if s == "AtCoder Land" else "No")

if __name__ == "__main__":
  main()