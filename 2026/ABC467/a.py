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
  H, W = map(int, input().split())

  if W * 10000 >= 25 * H * H:
    print("Yes")
  else:
    print("No")

if __name__ == "__main__":
  main()