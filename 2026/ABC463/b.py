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
  N, X = input().split()
  N = int(N)
  idx = ord(X) - 65

  s_list = [(input()) for _ in range(N)]

  ans = False

  for s in s_list:
    if s[idx] == "o":
      ans = True
      break

  print("Yes" if ans else "No")

if __name__ == "__main__":
  main()