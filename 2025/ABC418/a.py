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
  N = int(input())
  S = input()

  ans = len(S) >= 3 and S[-3:] == "tea"

  print("Yes" if ans else "No")

if __name__ == "__main__":
  main()