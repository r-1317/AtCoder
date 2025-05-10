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
  r, x = map(int, input().split())
  if x == 1:
    print("Yes" if 1600 <= r <= 2999 else "No")
  else:
    print("Yes" if 1200 <= r <= 2399 else "No")

if __name__ == "__main__":
  main()