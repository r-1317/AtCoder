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
  S = input()

  f = S[0]

  if S.count(f) == 1:
    print(f)
  else:
    for i in range(len(S)):
      if S[i] != f:
        print(S[i])

if __name__ == "__main__":
  main()