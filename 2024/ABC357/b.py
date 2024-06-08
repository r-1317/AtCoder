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
  n = len(s)
  upper = 0
  lower = 0

  for i in range(n):
    if s[i].isupper():
      upper += 1
    else:
      lower += 1

  if lower < upper:
    print(s.upper())
  else:
    print(s.lower())

if __name__ == "__main__":
  main()