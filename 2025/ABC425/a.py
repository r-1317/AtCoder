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

  ans = 0

  for i in range(1, N + 1):
    ans += (-1)**i * i**3

  print(ans)

if __name__ == "__main__":
  main()