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

  for i in range(1, N+1):
    print(i if i%3 else "Fizz")

if __name__ == "__main__":
  main()