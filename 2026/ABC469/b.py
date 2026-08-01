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
  S = "x" + input() + "x"

  ans = 0

  for i in range(0, N):
    ic(S[i:i+3])
    if S[i:i+3] == "xxx":
      ans += 1

  print(ans)

if __name__ == "__main__":
  main()