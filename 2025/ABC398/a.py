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

  ans = ["-"] * n

  if n%2:
    ans[n//2] = "="
  else:
    ans[n//2-1] = "="
    ans[n//2] = "="

  print(*ans, sep="")

if __name__ == "__main__":
  main()