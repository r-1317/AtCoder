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
  l, r = map(int, input().split())
  if (l and r) or ((not l) and (not r)):
    print("Invalid")
  elif l:
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  main()