import os
import sys

MyPC = os.path.basename(__file__) != "Main.py"
if MyPC:
  from icecream import ic
  ic.disable()
else:
  def ic(*args):
    return None

ic.enable() if MyPC else None

def main():
  a, b, C = map(int, input().split())

  x = 0
  y = 0

  for i in range(61):
    if C >> i & 1:
      if a >= b:
        x += 1 << i
        a -= 1
      else:
        y += 1 << i
        b -= 1

  if min(a, b) < 0 or a != b:
    print(-1)
    sys.exit()

  i = 0
  while a:
    if not(x >> i & 1 or y >> i & 1):
      x += 1 << i
      y += 1 << i
      a -= 1
    i += 1
    if i > 60:
      break

  if a > 0:
    print(-1)
    sys.exit()

  print(x, y)

if __name__ == "__main__":
  main()