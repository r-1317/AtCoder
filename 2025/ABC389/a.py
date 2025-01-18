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
  ic(s[0])
  ic(s[2])
  print(int(s[0])*int(s[2]))

if __name__ == "__main__":
  main()