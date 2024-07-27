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
  s_list = [input() for _ in range(n)]

  ans = True

  for i in range(n-2):
    if s_list[i] == s_list[i+1] == "sweet":
      ans = False
      break

  print("Yes" if ans else "No")

if __name__ == "__main__":
  main()