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
  n = int(input())
  a = n // 100
  b = n % 100 // 10
  c = n % 10

  bca = b * 100 + c * 10 + a
  cab = c * 100 + a * 10 + b

  print(bca, cab)

if __name__ == "__main__":
  main()