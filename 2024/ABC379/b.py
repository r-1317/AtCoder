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
  n, k = map(int, input().split())
  s = input()

  ans = 0
  count = 0
  
  for i in range(n):
    if s[i] == "O":
      count += 1
    else:
      count = 0
    if count == k:
      ans += 1
      count = 0

  print(ans)

if __name__ == "__main__":
  main()