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
  n = 2*10**5
  m = 10**5

  print(n, m)

  for i in range(m):
    print(i*2+1, i*2+2, 1)

if __name__ == "__main__":
  main()