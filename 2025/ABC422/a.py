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
  S = input()
  a = int(S[0])
  b = int(S[2])

  b += 1
  if b == 9:
    a += 1
    b = 1

  print(f"{a}-{b}")

if __name__ == "__main__":
  main()