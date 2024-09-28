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
  ans = 0

  for i in range(1,13):
    s = input()
    if len(s) == i:
      ans += 1

  print(ans)


if __name__ == "__main__":
  main()