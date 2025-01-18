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
  x = int(input())

  tmp = 1

  for i in range(1, 5*10**5):
    tmp *= i
    if tmp == x:
      print(i)
      break

if __name__ == "__main__":
  main()