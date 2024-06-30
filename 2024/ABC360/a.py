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
  r = 0
  m = 0

  for i in range(3):
    if s[i] == "R":
      r = i
    elif s[i] == "M":
      m = i

  print("Yes" if r < m else "No")

if __name__ == "__main__":
  main()