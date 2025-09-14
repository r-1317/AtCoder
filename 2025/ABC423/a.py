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
  X, C = map(int, input().split())

  ans = X // (1000+C)

  print(ans*1000)

if __name__ == "__main__":
  main()