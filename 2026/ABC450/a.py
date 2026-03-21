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

  for i in range(N, 1, -1):
    print(f"{str(i)},", end="")
  
  print(1)

if __name__ == "__main__":
  main()