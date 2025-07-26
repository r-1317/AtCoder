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
  N, L, R = map(int, input().split())
  S = input().strip()

  ans = True

  for i in range(L, R + 1):
    if S[i - 1] != "o":
      ans = False
      break

  print("Yes" if ans else "No")

if __name__ == "__main__":
  main()