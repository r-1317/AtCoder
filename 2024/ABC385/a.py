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
  a, b, c = map(int, input().split())
  flag = False
  if a == b == c:
    flag = True
  elif a+b == c or a+c == b or b+c == a:
    flag = True

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()