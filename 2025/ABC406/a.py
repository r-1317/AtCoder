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
  a, b, c, d = map(int, input().split())

  flag = True
  if a < c:
    flag = False
  elif a == c:
    if b < d:
      flag = False

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()