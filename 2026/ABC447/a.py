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
  N, M = map(int, input().split())

  max_m = N//2 + N%2

  print("Yes" if max_m >= M else "No")

if __name__ == "__main__":
  main()