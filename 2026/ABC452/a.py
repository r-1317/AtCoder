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
  M, D = map(int, input().split())

  if (M, D) in [(1, 7), (3, 3), (5, 5), (7, 7), (9, 9)]:
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  main()