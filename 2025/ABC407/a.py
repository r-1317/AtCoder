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
  a, b = map(int, input().split())
  x = int(a / b)

  ans = None
  min_diff = float('inf')

  for i in range(3):
    y = x + i
    diff = abs(a/b - y)
    if diff < min_diff:
      min_diff = diff
      ans = y

  print(ans)

if __name__ == "__main__":
  main()