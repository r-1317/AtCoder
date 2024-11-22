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
  n = int(input())
  s = input()

  s = "a" + s  # 1-indexedにする

  if n % 2 == 0:
    print("No")
    sys.exit()

  flag = True

  for i in range(1, (n+1) // 2):
    if s[i] != "1":
      flag = False
      break

  if s[(n+1) // 2] != "/":
    flag = False

  for i in range((n+1) // 2 + 1, n+1):
    if s[i] != "2":
      flag = False
      break

  print("Yes" if flag else "No")

if __name__ == "__main__":
  main()