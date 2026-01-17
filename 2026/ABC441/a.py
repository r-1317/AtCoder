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
  P, Q = map(int, input().split())
  X, Y = map(int, input().split())

  print("Yes" if P <= X < (P+100) and Q <= Y < (Q+100) else "No")

if __name__ == "__main__":
  main()