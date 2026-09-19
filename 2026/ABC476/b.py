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
  S = input()
  T = input()

  ans = True

  for i in range(N):
    if T[i] == "*":
      continue
    if S[i] != T[i]:
      ans = False
      break

  print("Yes" if ans else "No")

if __name__ == "__main__":
  main()