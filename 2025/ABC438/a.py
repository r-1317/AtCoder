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
  D, F = map(int, input().split())
  date = F

  while date <= D:
    date += 7

  print(date%D)

if __name__ == "__main__":
  main()