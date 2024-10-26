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

  if s.find("A") >= 0 and s.find("B") >= 0 and s.find("C") >= 0:
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  main()