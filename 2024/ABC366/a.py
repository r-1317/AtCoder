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
  n, t, a = map(int, input().split())

  ans = n//2 < t or n//2 < a

  print("Yes" if ans else "No")

if __name__ == "__main__":
  main()