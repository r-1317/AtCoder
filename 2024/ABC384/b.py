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
  n, rating = map(int, input().split())

  for i in range(n):
    d, a = map(int, input().split())
    if d == 1:
      if 1600 <= rating <= 2799:
        rating += a
    elif d == 2:
      if 1200 <= rating <= 2399:
        rating += a

  print(rating)

if __name__ == "__main__":
  main()