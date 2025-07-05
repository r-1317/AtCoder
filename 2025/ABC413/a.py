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
  n, m = map(int, input().split())
  a_list = list(map(int, input().split()))

  print("Yes" if sum(a_list) <= m else "No")

if __name__ == "__main__":
  main()