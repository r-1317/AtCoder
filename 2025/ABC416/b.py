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

  T = list(S)

  flag = False

  for i in range(len(S)):
    if T[i] == "." and not flag:
      T[i] = "o"
      flag = True
    elif T[i] == "#" and flag:
      flag = False

  print(*T, sep="")

if __name__ == "__main__":
  main()