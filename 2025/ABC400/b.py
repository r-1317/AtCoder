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

  x = 0

  for i in range(m+1):
    x += n**i
    if 10**9 < x:
      print("inf")
      exit()

  print(x)

if __name__ == "__main__":
  main()