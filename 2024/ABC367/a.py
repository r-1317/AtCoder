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

  if b < c:
    print("No" if b < a < c else "Yes")
  else:
    print("Yes" if c < a < b else "No")

if __name__ == "__main__":
  main()